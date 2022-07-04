'''
Save microblog entries
'''

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
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


class GitStorage(MicroblogStorage):
    '''
    Store microblog entries in a directory tracked by Git
    '''

    def __init__(self, directory):
        self.repo = git.Repo(directory)
        self.path = Path(directory)

    def save(self, entry):
        uid = self._new_uid()
        filename = self._path(uid)
        with filename.open('w') as out:
            yaml.dump(entry.dict(), out)
        log.debug(f'Saved microblog entry to {filename}')
        return uid

    def read(self, uid):
        filename = self._path(uid)
        log.debug(f'Reading {filename}')
        with filename.open() as file_:
            return MicroblogEntry(**yaml.load(file_))

    def _path(self, uid, suffix=None):
        dirname = f'{uid[:4]}'
        suffix = suffix or 'yml'
        filename = f'{uid}.{suffix}'
        return self.path / dirname / filename

    def _new_uid(self):
        now = datetime.now()
        year = now.strftime('%Y')
        timestamp = now.strftime('%Y%m%d_%H%M')
        while True:
            suffix = ''.join(random.choices(string.ascii_letters, k=6))
            uid = f'{timestamp}_{suffix}'
            path = self._path(uid)
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()  # will raise an Exception if file exists
                return uid
