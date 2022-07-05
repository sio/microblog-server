import pytest
import logging

from microblog import MicroblogEntry
from microblog.storage import GitStorage

def test_save(repo, caplog):
    caplog.set_level(logging.DEBUG)
    entry = MicroblogEntry(
        timestamp = '2012-12-19T06:01:17.171+00:00',
        author = 'Author McAuthorFace',
        content = 'Here is what I\'m having for breakfast: http://image.host/cool-picture.jpg',
    )
    storage = GitStorage(repo)

    try:
        initial_commit = storage.repo.head.commit
    except ValueError:
        initial_commit = None  # Reference at 'refs/heads/master' does not exist
    uid = storage.save(entry)
    last_commit = storage.repo.head.commit
    assert initial_commit != last_commit
    assert last_commit

    returned = storage.read(uid)
    assert entry == returned
    assert entry.uid == returned.uid

    assert uid == next(storage.uids())
    for item in storage:
        assert entry == item
        assert entry.uid == item.uid
        break  # we check only the newest item
