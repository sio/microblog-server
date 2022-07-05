'''
Acquire microblog entries
'''

from abc import ABC, abstractmethod

from telegram.ext import (
        ApplicationBuilder,
        CommandHandler,
        MessageHandler,
        filters,
)
from . import MicroblogEntry


class MicroblogInput(ABC):
    '''
    Base class for microblog inputs
    '''

    @abstractmethod
    def run(self):
        '''Run indefinitely, wait for microblog inputs and save entries to storage'''


class TelegramInput(MicroblogInput):
    '''
    Receive microblog entries via Telegram bot
    '''

    def __init__(self, storage, token, allowed_users=None):
        self.storage = storage

        if allowed_users is None:
            allowed_users = set()
        self.allowed_users = set(allowed_users)

        self.app = ApplicationBuilder().token(token).build()
        for command, handler in dict(
            hello = self.hello,
            start = self.start,
        ).items():
            self.app.add_handler(CommandHandler(command, handler))
        self.app.add_handler(MessageHandler(
            filters.Chat(username=self.allowed_users) & ~filters.COMMAND,
            self.microblog
        ))

    def run(self):
        self.app.run_polling()

    def allowed(self, update):
        '''Check if we should allow to process this message'''
        return update.effective_user.username in self.allowed_users

    async def microblog(self, update, context):
        '''Save microblog message to storage'''
        user = update.effective_user
        message = update.message
        entry = MicroblogEntry(
            timestamp=message.date,
            author=f'{user.first_name} {user.last_name}'.strip(),
            content=message.text,
            markup='plaintext',
        )
        self.storage.save(entry)

    async def hello(self, update, context):
        if not self.allowed(update):
            return
        await update.message.reply_text(f'Hello {update.effective_user.first_name}')

    async def start(self, update, context):
        if self.allowed(update):
            message = f'Hello {update.effective_user.first_name}'
        else:
            message = f'Unfortunately, you are not authorized to interact with this bot'
        await update.message.reply_text(message)
