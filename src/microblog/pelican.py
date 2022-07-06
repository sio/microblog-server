from hashlib import sha1 as checksum
from pathlib import Path
from shutil import copyfileobj

from pelican import signals
from pelican.generators import Generator

from . import log


def get_generators(pelican):
    return MicroblogGenerator


def register():
    signals.get_generators.connect(get_generators)


class MicroblogGenerator(Generator):
    '''Read git microblog and generate output with Pelican'''

    def generate_context(self):
        if 'MICROBLOG' not in self.settings:
            raise ValueError('required pelican variable is not defined: MICROBLOG')
        self.microblog = self.settings['MICROBLOG']
        self.index_url = self.settings.get(
            'MICROBLOG_INDEX_URL',
            'micro/'
        )
        self.index_dest = self.settings.get(
            'MICROBLOG_INDEX_SAVE_AS',
            self.index_url if self.index_url.endswith('.html') else f'{self.index_url}/index.html'
        )
        self.micro_url = self.settings.get(
            'MICROBLOG_PAGE_URL',
            'micro/{uid}/'
        )
        self.micro_dest = self.settings.get(
            'MICROBLOG_PAGE_SAVE_AS',
            self.micro_url if self.micro_url.endswith('.html') else f'{self.micro_url}/index.html'
        )
        pagination = self.settings['PAGINATED_TEMPLATES']
        if 'micros' not in pagination:
            pagination['micros'] = 100  # default settings

    def generate_output(self, writer):
        context = self.context.copy()
        context['microblog'] = self.microblog
        context['attachment_url'] = attachment_url
        uids = list(self.microblog.uids())
        writer.write_file(
            name=self.index_dest,
            template=self.get_template('micros'),
            context=context,
            relative_urls=self.settings['RELATIVE_URLS'],
            paginated={'micros': uids},
            template_name='micros',
            url=self.index_url,
        )
        for uid in uids:
            context['micro'] = entry = self.microblog.read(uid)
            save_attachments(writer, self.microblog, entry)
            writer.write_file(
                name=self.micro_dest.format(uid=uid),
                template=self.get_template('micro'),
                context=context,
                relative_urls=self.settings['RELATIVE_URLS'],
                template_name='micro',
                url=self.micro_url.format(uid=uid),
            )

def save_attachments(writer, microblog, entry):
    for num, name in enumerate(microblog.attached_names(entry), start=1):
        url = attachment_url(entry.uid, num)
        output = Path(writer.output_path) / url
        output.parent.mkdir(parents=True, exist_ok=True)
        with microblog.attachment(entry, name) as attach:
            with output.open('wb') as out:
                copyfileobj(attach, out)
                log.debug(f'Saved attachment {name} to {output}')

def attachment_url(entry_uid, attachment_num):
    uid_hash = checksum(entry_uid.encode()).hexdigest()
    return f'micro/img/{uid_hash}-{attachment_num}'
