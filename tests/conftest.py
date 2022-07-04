from tempfile import TemporaryDirectory
from pathlib import Path

import pytest

import git

@pytest.fixture(scope='session')
def repo():
    with TemporaryDirectory(prefix='microblog_test_') as temp:
        repo = git.Repo.init(temp)
        yield Path(temp)
