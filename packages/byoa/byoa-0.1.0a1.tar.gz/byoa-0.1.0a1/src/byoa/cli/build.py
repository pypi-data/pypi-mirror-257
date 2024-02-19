"""Build command"""

import os
import subprocess

import click
import docker
import toml

from byoa.config.manifest import Manifest, check_manifest


@click.group("build", short_help="builds the processor")
def build():
    """Build the processor"""


@build.command("image", short_help="builds a processor image")
@check_manifest
def build_image():
    """Builds the processor as a Docker image"""

    manifest = Manifest()
    docker_client = docker.from_env()

    click.echo("Building image...", nl=False)
    docker_client.images.build(path="./", tag=manifest.slug)
    click.echo("DONE !")


@build.command("wheel", short_help="builds a processor wheel")
@check_manifest
def build_wheel():
    """Builds the processor package as a wheel"""

    command = "python -m pip wheel --wheel-dir=dist --no-deps ."
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

    with open("pyproject.toml", "r", encoding="utf-8") as f:
        config = toml.load(f)

    if result.returncode == 0:
        # output_lines = result.stdout.split()
        click.echo(
            "Setup file generated successfully.\nPlease use the command below to install it:"
        )
        file_install = (
            config["project"]["name"] + "-" + config["project"]["version"] + "-py3-none-any.whl"
        )
        folder_path = "dist/"

        file_path = os.path.join(folder_path, file_install)

        if os.path.exists(file_path):
            click.secho("pip install dist/" + file_install, bold=True)
        else:
            click.secho("pip install dist/your_file.whl", bold=True)

    else:
        click.echo("An error occured during the setup file generation, please see error below:")
        click.echo(result.stderr)
