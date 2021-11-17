# Contributing

## pre-requisites

1. [python3.9+](https://realpython.com/installing-python/)
2. [poetry>=1.2](https://python-poetry.org/docs/master/#installation)
3. docker
4. [The Digital Ocean CLI](https://docs.digitalocean.com/reference/doctl/how-to/install/)

```sh
# this currently requires installing a preview poetry version
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py \
    | POETRY_VERSION=1.2.0a2 POETRY_PREVIEW=1 python -
```

## Set up virtual environment

Create virtual environment and install dependencies

```sh
poetry install
```

Activate virtual environment

```sh
poetry shell
```

## Install pre-commit hooks

```sh
pre-commit install
```

## Run Tests

```sh
pytest
```

## Build and Push Docs (not actually worth doing)

In order to be able to share pretty mkdocs docs with the aspiration team without them being public, I ended up settling on using oauth2-proxy as a proxy server, configured to use github for authentication and authorization. The infrastructure for this is kind of a mess, and it wasn't designed to be reusable.

However, if you do want to deploy this for some reason, you'll need

1. A dockerhub account that you can push images to.
2. A digital ocean account with billing enabled.
3. An existing Digital Ocean app with an app ID (this is the biggest problem with this script tbh, but I don't have time to fix it up right now). I just did this through the app.
4. To set the `redirect_url` field in `docs-server/oauth2-proxy.cfg` to "{the url of youy digital ocean deployment}/oauth2/callback"
5. To set the following environment variables (I recommend using `direnv`, copying `cp .template.envrc .envrc`, and adding your secrets to `.envrc`)
   1. `DO_APP_ID`
      1. The ID of your Digital Ocean App. Can be acquired with
      ```sh
      doctl app list
      ```
   2. `CLIENT_SECRET` (from the [oauth2-proxy github provider docs](https://oauth2-proxy.github.io/oauth2-proxy/docs/configuration/oauth_provider/#github-auth-provider))
      1. [Create a new github app](https://github.com/settings/developers)
      2. Under `Authorization callback URL`, enter the oauth callback for your digital ocean deployment (https://some-name.ondigitalocean.app/oauth2/callback)
   3. `COOKIE_SECRET`
      1. The oauth2-proxy docs includes a [list of options](https://oauth2-proxy.github.io/oauth2-proxy/docs/configuration/overview#generating-a-cookie-secret) for generating secure cookie secrets
   4. (Optional if you're me) - `DOCKER_ID`
      1. your dockerhub user ID
   5. (Optional if you're me) - `GITHUB_REPO`
      1. Of the form `owner/name`
      2. Any _contributor_ in this repo will be able to authenticate to the oauth2-proxy server
   6. (Optional if you're me) - `GITHUB_USERS`
      1. A comma-separated list of github user IDs
      2. Anyone in this list will be able to authenticate to the oauth2-proxy server (this is necessary if the repo is owned by a user, since that user can't be added as a _contributor_)
6. To the `client_id` field in `docs-server/oauth2-proxy.cfg` to the client_id for your github app.

Once you've done all of that (assuming I haven't missed any other steps), it's as simple as

```sh
poetry shell
nox -s build_and_push_docs
```
