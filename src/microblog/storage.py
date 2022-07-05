'''
Save microblog entries
'''

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from textwrap import shorten
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

    def __iter__(self):
        return (self.read(uid) for uid in self.uids())


class GitStorage(MicroblogStorage):
    '''
    Store microblog entries in a directory tracked by Git
    '''

    RECORD_EXTENSION = '.yml'

    def __init__(self, directory):
        self.repo = git.Repo(directory)
        self.path = Path(directory)

    def save(self, entry):
        uid = self._new_uid()
        filename = self._path(uid)
        with filename.open('w') as out:
            yaml.dump(entry.dict(), out)
        log.debug(f'Saved microblog entry to {filename}')
        repo = self.repo
        repo.index.add([str(filename)])
        message = f'Microblog: {shorten(entry.content, width=40, placeholder="…")}'
        commit = repo.index.commit(message)
        if repo.active_branch.tracking_branch():
            for remote in repo.remotes:
                try:
                    remote.push().raise_if_error()
                except Exception as e:
                    log.exception(f'Error while pushing to remote: {remote}')
        else:
            log.warning(f'Not pushing commit {commit}, no tracking branch configured')
        return uid

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

    def _new_uid(self):
        now = datetime.now(timezone.utc)
        timestamp = now.strftime('%Y%m%d_%H%M%S_%f')
        while True:
            suffix = ''.join(random.choices(string.ascii_letters, k=6))
            uid = f'{timestamp}_{suffix}'
            path = self._path(uid)
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()  # will raise an Exception if file exists
                return uid
