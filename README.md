# Microblog backend

Python backend for a low-volume personal microblog.

Input server (Telegram bot) waits for user to post new microblog entries and
saves them to storage (git repo). Entries can be fetched from storage by using
provided Python library. There is also a plugin for Pelican to render
microblog entries for a static web site.

Input server and storage engine should be easy to replace or add new
implementations in future.

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
