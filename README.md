# Microblog server

Python backend for a low-volume personal microblog.

Input server (Telegram bot) waits for user to post new microblog entries and
saves them to storage (git repo). Entries can be fetched from storage via
provided Python library. There is also a plugin for Pelican to render
microblog entries on a static web site.

Input server and storage engine should be easy to replace or add new
implementations in future.


## Installation

- Python package is published at PyPI: <https://pypi.org/project/microblog-server/>
    - Install with `pip install microblog-server`
    - Make sure that `git` is available in $PATH

- Ready to go [Docker image] is also available

[Docker image]: container/README.md


## Usage

#### Running input server

- Commandline entrypoint: `microblog`
- Configuration is done via environment variables:
    - `MICROBLOG_STORAGE`: Path to a local checkout of git repository that
      stores the microblog
    - `MICROBLOG_TOKEN`: Telegram bot token
    - `MICROBLOG_USERS`: Comma-separated list of Telegram accounts allowed to
      interact with the bot

#### Using Python library to read microblog from storage

See the [source code](src/microblog/storage.py)

#### Rendering static web site

See [Pelican docs] for general information on using static site generator.

Plugin configuration:

```python3
# pelicanconf.py
import microblog.pelican
import microblog.storage
PLUGINS = [
    microblog.pelican,
]
MICROBLOG = microblog.storage.GitStorage('./path/to/local/copy/of/git/repo/')
```

Your theme is expected to provide the following templates:

- `micros` for paginated microblog index
  ([example](https://github.com/sio/potyarkin.ml/blob/5afe24bd07f3f065b3ab8f7026960757748d0bfc/content/templates/micros.html))
- `micro` for individual microblog entries
  ([example](https://github.com/sio/potyarkin.ml/blob/5afe24bd07f3f065b3ab8f7026960757748d0bfc/content/templates/micro.html))

Check [plugin source] for further information.
See author's site [configuration] for further examples.

[Pelican docs]: https://docs.getpelican.com/en/latest/
[plugin source]: src/microblog/pelican.py
[configuration]: https://github.com/sio/potyarkin.ml/blob/5afe24bd07f3f065b3ab8f7026960757748d0bfc/pelicanconf.py#L146-L148


## License and copyright

Copyright 2022 Vitaly Potyarkin

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
