from dataclasses import dataclass, asdict
from datetime import datetime

from . import renderers
from .logging import log


@dataclass
class MicroblogEntry:
    timestamp: datetime
    author: str
    content: str
    markup: str = 'plaintext'

    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
        if not isinstance(self.timestamp, datetime):
            raise ValueError(f'unexpected timestamp object: {self.timestamp!r}')
        if not hasattr(renderers, self.markup):
            raise ValueError(f'unsupported markup format: {self.markup}')

    @property
    def html(self):
        if not hasattr(self, '_html'):
            self._html = self.render()
        return self._html

    def render(self):
        renderer = getattr(renderers, self.markup)
        return renderer(self.content)

    def isotime(self):
        return self.timestamp.isoformat()

    def dict(self):
        output = asdict(self)
        output['timestamp'] = self.isotime()
        return output
