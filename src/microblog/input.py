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
from . import MicroblogEntry, log


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

    PHOTO_CAPTION_MAX_DELAY_SECONDS = 60

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
        message = update.effective_message
        entry = MicroblogEntry(
            timestamp=message.date,
            author=f'{user.first_name} {user.last_name}'.strip(),
            content=message.text or message.caption or '',
            markup='plaintext',
        )
        log.debug(f'Current:  {entry.uid}')

        prev = self.storage.latest()
        if prev:
            log.debug(f'Previous: {prev.uid}')
            delay = entry.timestamp - prev.timestamp
            max_delay = self.PHOTO_CAPTION_MAX_DELAY_SECONDS
            if message.photo and not entry.content \
            and 0 <= delay.total_seconds() <= max_delay \
            and entry.author == prev.author:
                entry = prev
                log.debug('Attaching photos to previous microblog entry')
        uid = self.storage.save(entry)
        log.debug(f'Saved microblog entry: {uid}')

        photos_seen = set()
        for photo in sorted(message.photo, key=lambda x: x.width, reverse=True):
            name = photo.file_unique_id[:10]  # TODO: how do we distinguish between multiple sizes of the same pic?
            if name in photos_seen:
                log.debug(f'Skipping photo: {name}')
                continue
            log.debug(f'Saving photo: {name}')
            photos_seen.add(name)
            remote = await photo.get_file()
            with self.storage.attachment(entry, name=name, writable=True) as local:
                await remote.download(out=local)
                log.debug(f'Downloaded photo: {name}')

        await message.reply_text('Ok')

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
