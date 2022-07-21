# Docker container for microblog-server

Container image for this repo is available at `ghcr.io/sio/microblog-server`

## Environment variables

This container will fail to start without the following variables:

- `MICROBLOG_USERS`
- `MICROBLOG_TOKEN`
- `MICROBLOG_REPO_URL`: Git repo that will be used to store microblog entries.
  Required only for initial clone, you may initialize the repo manually prior to
  starting the container.


## Filesystem paths

This container expects to find data at some predefined paths. You may want to
use bind mounts or Docker volumes for this.

- `/storage`: Local checkout of `$MICROBLOG_REPO_URL`. Will be created
  automatically if not exists.
  This path is hardcoded  as value for `$MICROBLOG_STORAGE`
- `/storage.key`: SSH key authorized to push to `$MICROBLOG_REPO_URL`
