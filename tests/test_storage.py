import pytest

from microblog import MicroblogEntry
from microblog.storage import GitStorage

def test_save(repo):
    entry = MicroblogEntry(
        timestamp = '2012-12-19T06:01:17.171+00:00',
        author = 'Author McAuthorFace',
        content = 'Here is what I\'m having for breakfast: http://image.host/cool-picture.jpg',
    )
    storage = GitStorage(repo)
    uid = storage.save(entry)
    returned = storage.read(uid)
    assert entry == returned
