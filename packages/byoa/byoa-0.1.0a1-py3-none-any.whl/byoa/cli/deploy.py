"""Deploy command"""

import json

import click
import docker
import requests

from byoa.config.context import ENDPOINT_KEY, REGISTRY_KEY, get_context_value
from byoa.config.manifest import Manifest, check_manifest
from byoa.exceptions import APIError, MissingContextValue
from byoa.importer import get_model_class_from_string

_NOT_FOUND = 400
_FOUND = 200


def _login_to_docker(docker_client: docker.DockerClient, registry: str):
    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)

    click.echo("Login to registry... ", nl=False)
    result_login = docker_client.login(username=username, password=password, registry=registry)
    click.echo(result_login["Status"])


def _register_version(processor_id: str, data: dict, endpoint: str, version: str):
    try:
        response = requests.get(
            f"{endpoint}/processors/{processor_id}/versions/{version}", timeout=60
        )
    except requests.exceptions.RequestException as e:
        raise APIError(f'Cannot get version {version}: "{e}"') from e

    if response.status_code == _NOT_FOUND:
        click.echo(f"Registering processor {processor_id} version {version}...", nl=False)
        response = requests.post(
            f"{endpoint}/processors/{processor_id}/versions",
            json=data,
            timeout=60,
        )
        click.echo(response.reason)

    elif response.status_code == _FOUND:
        click.echo(f"Version {version} already exists")


def _register_processor(processor_id: str, data: dict, endpoint: str):
    try:
        response = requests.get(f"{endpoint}/processors/{processor_id}", timeout=60)

    except requests.exceptions.RequestException as e:
        raise APIError(f'Cannot get processor {processor_id}: "{e}"') from e

    if response.status_code == _NOT_FOUND:
        click.echo(f"Registering processor {processor_id}...", nl=False)
        response = requests.post(f"{endpoint}/processors", json=data, timeout=60)
        click.echo(response.reason)

    elif response.status_code == _FOUND:
        click.echo(f"Updating processor {processor_id}...", nl=False)
        response = requests.patch(f"{endpoint}/processors/{processor_id}", json=data, timeout=60)
        click.echo(response.reason)


@click.command("deploy", short_help="deploys the processor")
@click.option(
    "--registry",
    help="Container registry name",
    envvar="BYOA_CONTAINER_REGISTRY",
    show_envvar=True,
    default=lambda: get_context_value(REGISTRY_KEY),
)
@click.option(
    "--endpoint",
    help="BYOA API endpoint",
    envvar="BYOA_ENDPOINT",
    show_envvar=True,
    default=lambda: get_context_value(ENDPOINT_KEY),
)
@click.option("--profile", help="Profile to use for environment values")
@click.option(
    "--input_model",
    default="schemas.output_schema:OutputModel",
    show_default=True,
    help="Output model class",
)
@click.option(
    "--output_model",
    default="schemas.input_schema:InputModel",
    show_default=True,
    help="Input model class",
)
@check_manifest
def deploy(profile: str, registry: str, endpoint: str, input_model: str, output_model: str):
    """Registers and deploys the processor"""

    if profile:
        _registry = get_context_value(REGISTRY_KEY, profile, registry)
        _endpoint = get_context_value(ENDPOINT_KEY, profile, endpoint)

        if _endpoint is None:
            raise MissingContextValue(ENDPOINT_KEY)
        if _registry is None:
            raise MissingContextValue(REGISTRY_KEY)

        endpoint = _endpoint
        registry = _registry

    manifest = Manifest()

    with open("VERSION", "r", encoding="utf-8") as f:
        version = f.read()

    docker_client = docker.from_env()

    input_class = get_model_class_from_string(input_model)
    output_class = get_model_class_from_string(output_model)

    data = {
        "id": manifest.slug,
        "name": manifest.name,
        "summary": manifest.summary,
        "description": manifest.description,
        "input": json.dumps(input_class.model_json_schema()),
        "output": json.dumps(output_class.model_json_schema()),
        "author": manifest.author,
    }
    _register_processor(manifest.slug, data, endpoint)

    data = {
        "image_uri": f"{_registry}/byoa/processor/{manifest.slug}:v{version}",
        "version": version,
    }
    _register_version(manifest.slug, data, endpoint, version)

    click.echo("Building image... ", nl=False)
    docker_client.images.build(
        path="./", tag=f"{_registry}/byoa/processor/{manifest.slug}:v{version}"
    )
    click.echo("DONE !")

    if click.confirm("Do you need to login to your container registry ?", True):
        _login_to_docker(docker_client, registry)

    click.echo("Pushing the image... ", nl=False)
    docker_client.images.push(f"{_registry}/byoa/processor/{manifest.slug}", tag=f"v{version}")
    click.echo("DONE !")
