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
    app_id = os.environ["DO_APP_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    cookie_secret = os.environ["COOKIE_SECRET"]
    github_token = os.environ["GITHUB_TOKEN"]
    docker_id = os.environ.get("DOCKER_ID", "zanedufour")
    github_repo = os.environ.get("GITHUB_REPO_OWNER", "zdog234/aspiration")

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
        f"docker.io/{docker_id}/aspiration_proxy:{tag}",
        external=True,
    )
    session.run(
        "docker",
        "push",
        f"docker.io/{docker_id}/aspiration_proxy:{tag}",
        external=True,
    )
    with digital_ocean_spec(
        client_secret=client_secret,
        cookie_secret=cookie_secret,
        tag=tag,
        docker_id=docker_id,
        github_repo=github_repo,
        github_token=github_token,
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
def digital_ocean_spec(
    *,
    client_secret,
    cookie_secret,
    tag: str,
    docker_id: str,
    github_repo: str,
    github_token: str,
):
    with TemporaryDirectory() as td:
        config = {
            "name": "aspiration-proxy",
            "services": [
                {
                    "name": "proxy",
                    "image": {
                        "registry_type": "DOCKER_HUB",
                        "registry": f"{docker_id}",
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
                            # I haven't been able to test this. (owner can't be a collaborator)
                            f"--github-repo={github_repo}",
                            f"--cookie-secret={cookie_secret}",
                            f"--github-token={github_token}",
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
