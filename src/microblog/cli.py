import os

from .input import TelegramInput
from .storage import GitStorage

def main():
    storage = GitStorage(os.environ['MICROBLOG_STORAGE'])
    allowed = os.environ.get('MICROBLOG_USERS')
    if allowed:
        allowed = [u.lstrip('@') for u in allowed.split(',')]
    server = TelegramInput(
        storage=storage,
        token=os.environ['MICROBLOG_TOKEN'],
        allowed_users=allowed,
    )
    server.run()
