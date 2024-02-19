"""Run command"""

import click
import docker

from byoa.config.manifest import Manifest, check_manifest


@click.command("run", short_help="executes the processor")
@click.option(
    "--entrypoint",
    "-e",
    type=click.Choice(["api", "cli"], case_sensitive=False),
    default="cli",
    help="How the processor is started",
)
@click.option("--build", "-b", is_flag=True, help="Build the image before running")
@check_manifest
def run_processor(entrypoint: str, build: bool):
    """Runs the processor's Docker image"""

    manifest = Manifest()
    docker_client = docker.from_env()

    if build:
        click.echo("Building image...", nl=False)
        image, _ = docker_client.images.build(path="./", tag=manifest.slug)
        click.echo("DONE !")
    else:
        image = docker_client.images.get(manifest.slug)

    click.echo(f"Running image {image.tag}")
    if entrypoint == "api":
        docker_client.containers.run(
            image, environment=["RUN_MODE_ENV=API"], ports={"80": 8081}, detach=True
        )
        click.echo(
            "API running on http://localhost:8081. "
            "Swagger UI available at http://localhost:8081/docs",
        )

    else:
        raw_output = docker_client.containers.run(image)
        click.echo(raw_output)
