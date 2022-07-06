'''
Save microblog entries
'''

from abc import ABC, abstractmethod
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from textwrap import shorten
from threading import Thread
from time import sleep
import random
import string

import git

from . import (
    MicroblogEntry,
    log,
    yaml,
)


class MicroblogStorage(ABC):
    '''
    Base class for microblog storage
    '''
    @abstractmethod
    def save(self, entry: MicroblogEntry) -> str:
        '''Save microblog entry to persistent storage'''
        return uid

    @abstractmethod
    def read(self, uid) -> MicroblogEntry:
        '''Read microblog entry from storage'''

    @abstractmethod
    def uids(self):
        '''Yield saved uids in reverse chronological order'''

    @abstractmethod
    def attachment(self, entry):
        '''Context manager that yields a file-like objects for writing attachments to'''

    def latest(self):
        '''Return the latest microblog entry'''
        try:
            return next(iter(self))
        except StopIteration:
            return None

    def __iter__(self):
        return (self.read(uid) for uid in self.uids())


class GitStorage(MicroblogStorage):
    '''
    Store microblog entries in a directory tracked by Git
    '''

    RECORD_EXTENSION = '.yml'
    GIT_PUSH_MIN_DELAY_SECONDS = 30

    def __init__(self, directory):
        self.repo = git.Repo(directory)
        self.path = Path(directory)
        self._actor = git.Actor('microblog', '')
        Thread(target=self._pusher, daemon=True).start()

    def save(self, entry):
        uid = entry.uid
        filename = self._path(uid)
        filename.parent.mkdir(parents=True, exist_ok=True)
        with filename.open('w', newline='\n') as out:
            yaml.dump(entry.dict(), out)
        log.debug(f'Saved microblog entry to {filename}')
        message = f'Microblog: {shorten(entry.content, width=40, placeholder="…")}'
        self._commit(filename, message)
        return uid

    @contextmanager
    def attachment(self, entry, name=None, writable=False):
        path = self._path(entry.uid, suffix=name)
        if not path.parent.exists():
            raise RuntimeError(f'Can not save attachments for unsaved entry: {entry.uid}')
        with open(path, 'wb' if writable else 'rb') as f:
            yield f
        self._commit(path, f'Attachment: {path.name}')

    def read(self, uid):
        filename = self._path(uid)
        log.debug(f'Reading {filename}')
        with filename.open() as file_:
            return MicroblogEntry(**yaml.load(file_))

    def uids(self):
        extension = self.RECORD_EXTENSION
        for directory in sorted(self.path.iterdir(), reverse=True):
            if not directory.is_dir():
                continue
            for filename in sorted(directory.glob(f'*{extension}'), reverse=True):
                if filename.is_dir():
                    continue
                yield filename.name[:-len(extension)]

    def _path(self, uid, suffix=''):
        dirname = f'{uid[:6]}'
        extension = self.RECORD_EXTENSION
        if suffix:
            suffix = f'+{suffix}'
        filename = f'{uid}{extension}{suffix}'
        return self.path / dirname / filename

    def _commit(self, path, message=''):
        repo = self.repo
        if not isinstance(path, Path):
            path = Path(path)
        repo.index.add([str(path.relative_to(self.path))])
        if not message:
            message = str(path)
        commit = repo.index.commit(message, author=self._actor, committer=self._actor)
        for parent in commit.parents:
            if commit.tree != parent.tree:
                break
        else:
            if commit.parents:
                log.debug(f'Reverting empty commit: {commit}')
                repo.active_branch.commit = parent

    def _push(self):
        repo = self.repo
        local_branch = repo.active_branch
        remote_branch = repo.active_branch.tracking_branch()
        if remote_branch:
            if remote_branch.commit == local_branch.commit:
                return
            for remote in repo.remotes:
                try:
                    remote.push().raise_if_error()
                except Exception as e:
                    log.exception(f'Error while pushing to remote: {remote}')
        else:
            log.warning(f'Not pushing, no tracking branch configured')

    def _pusher(self):
        '''Thread that pushes changes regularly'''
        while True:
            self._push()
            sleep(self.GIT_PUSH_MIN_DELAY_SECONDS)
