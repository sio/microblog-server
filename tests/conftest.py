from tempfile import TemporaryDirectory
from pathlib import Path
from time import sleep
import os
import sys

import pytest

import git

@pytest.fixture(scope='session')
def repo():
    temp = TemporaryDirectory(prefix='microblog_test_')
    repo = git.Repo.init(temp.name)
    yield Path(temp.name)
    retries = 3
    while retries:
        try:
            temp.cleanup()
            break
        except OSError: # WinError 32
            sleep(1)
            retries -= 1
            temp.cleanup()


# Tox clears USERNAME on Windows leading to errors in getpass.getuser()
if sys.platform == 'win32' and 'USERNAME' not in os.environ:
    os.environ['USERNAME'] = 'microblog-test'
