from pathlib import Path
import datetime as dt
import os
from contextlib import contextmanager
import nox
from tempfile import TemporaryDirectory
import shlex
import yaml


@nox.session
def build_docs_server(session):
    """Build oauth2-proxy image, push to dockerhub, then deploy on digital ocean"""
    app_id = os.environ.get("DO_APP_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    cookie_secret = os.environ.get("COOKIE_SECRET")

    # This is here because I'm using a prerelease version of poetry
    session.install("git+https://github.com/python-poetry/poetry.git@1.2.0a2")
    session.install(".[docs]")

    session.run("mkdocs", "build")

    tag = generate_docker_tag()
    session.run(
        "docker",
        "build",
        ".",
        "--file",
        "docs-server/Dockerfile",
        "-t",
        f"docker.io/zanedufour/aspiration_proxy:{tag}",
        external=True,
    )
    session.run(
        "docker",
        "push",
        f"docker.io/zanedufour/aspiration_proxy:{tag}",
        external=True,
    )
    with digital_ocean_spec(
        client_secret=client_secret, cookie_secret=cookie_secret, tag=tag
    ) as spec:
        session.run(
            "doctl",
            "apps",
            "update",
            f"--spec={spec}",
            app_id,
            external=True,
        )


@contextmanager
def digital_ocean_spec(*, client_secret, cookie_secret, tag: str):
    github_users = ["zdog234"]
    with TemporaryDirectory() as td:
        config = {
            "name": "aspiration-proxy",
            "services": [
                {
                    "name": "proxy",
                    "image": {
                        "registry_type": "DOCKER_HUB",
                        "registry": "zanedufour",
                        "repository": "aspiration_proxy",
                        "tag": tag,
                    },
                    "run_command": shlex.join(
                        [
                            "/bin/oauth2-proxy",
                            "--config",
                            "./oauth2-proxy.cfg",
                            f"--client-secret={client_secret}",
                            "--provider=github",
                            f"--github-user={','.join(github_users)}",
                            # I haven't been able to get this github_repo flag to work
                            "--github-repo",
                            "zdog234/aspiration",
                            f"--cookie-secret={cookie_secret}",
                        ]
                    ),
                    "routes": [{"path": "/"}, {"path": "/ping"}],
                }
            ],
        }
        fp = Path(td) / "digital-ocean.yml"
        with open(fp, "w") as file:
            yaml.safe_dump(config, file)

        yield fp


def generate_docker_tag() -> str:
    """Generate a unique docker tag with the current timestamp
    This is necessary because digital ocean seems to have imagePull
    set to something other than `always`, with no way to change it.
    """
    return dt.datetime.now().strftime("%Y.%m.%d.%H.%M.%S")
