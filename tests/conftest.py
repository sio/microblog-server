from tempfile import TemporaryDirectory
from pathlib import Path
import os
import sys

import pytest

import git

@pytest.fixture(scope='session')
def repo():
    with TemporaryDirectory(prefix='microblog_test_') as temp:
        repo = git.Repo.init(temp)
        yield Path(temp)


# Tox clears USERNAME on Windows leading to errors in getpass.getuser()
if sys.platform == 'win32' and 'USERNAME' not in os.environ:
    os.environ['USERNAME'] = 'microblog-test'
