'''
Convert different markups to HTML
'''

import html
import re

import markdown as md


URL = re.compile(r'((?:https?|mailto|ftp|gopher|gemini)://\S+)', re.IGNORECASE)


def plaintext(text, escape=html.escape):
    output = []
    for paragraph in text.split('\n\n'):
        if not paragraph.strip():
            continue
        chunks = []
        for chunk in URL.split(paragraph):
            if not chunk.strip():
                continue
            if URL.fullmatch(chunk):
                chunks.append(f'<a href="{chunk}">{escape(chunk)}</a>')
            else:
                chunks.append(escape(chunk))
        paragraph = '\n'.join(chunks)
        output.append(f'<p>{paragraph}</p>')
    return '\n'.join(output)



_markdown_extension_configs={
    'markdown.extensions.codehilite': {
        'css_class': 'highlight',
        'guess_lang': False,
    },
    'markdown.extensions.extra': {},
    'markdown.extensions.meta': {},
    'markdown.extensions.sane_lists': {},
    'pymdownx.magiclink': {},
    'pymdownx.saneheaders': {},
}
Markdown = md.Markdown(
    output_format='html5',
    extensions=list(_markdown_extension_configs),
    extension_configs=_markdown_extension_configs,
)
def markdown(text):
    '''Render HTML from Markdown text'''
    return Markdown.convert(text)
