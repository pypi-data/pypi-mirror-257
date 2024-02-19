"""Init command"""

from pathlib import Path

import click
from cookiecutter.main import cookiecutter
from slugify import slugify

from byoa.config.manifest import Manifest


def _get_project_slug():
    return slugify(click.get_current_context().params["name"], separator="_")


def _get_project_repo():
    return slugify(click.get_current_context().params["name"])


@click.command("init", short_help="creates a new processor project")
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path, writable=True),
    default=".",
)
@click.option("--advanced", "-a", is_flag=True, help="Creates an advanced project structure")
@click.option("--name", prompt=True, required=True, help="Name of the processor")
@click.option(
    "--slug",
    prompt=True,
    default=_get_project_slug,
    help="Human-readable, unique identifier of the processor",
)
@click.option(
    "--repository",
    prompt=True,
    default=_get_project_repo,
    help="The project's repository name",
)
@click.option(
    "--summary", prompt=True, default="", help="A short sentence describing the processor"
)
@click.option("--description", prompt=True, default="", help="Description of the processor")
@click.option("--author", prompt=True, default="", help="Author(s) of the project")
def init_processor(
    directory: Path,
    advanced: bool,
    name: str,
    slug: str,
    repository: str,
    summary: str,
    description: str,
    author: str,
):
    # pylint: disable=too-many-arguments
    """
    Creates a new BYOA project in the current directory or in DIRECTORY if specified.
    """

    cookiecutter(
        "https://github.com/GEOSYS/analytic-processor-template",
        no_input=True,
        extra_context={
            "project_name": name,
            "project_repo": repository,
            "project_slug": slug,
            "author_name": author,
            "description": description,
            "mode": "advanced" if advanced else "basic",
        },
        output_dir=directory,
        checkout="71cee9248ae18d96f4b970ab944c1fb625240243",
    )

    click.echo("Create byoa manifest file")
    manifest = Manifest(from_file=False)
    manifest.set("name", name)
    manifest.set("slug", slug)
    manifest.set("summary", summary)
    manifest.set("description", description)
    manifest.set("author", author)
    manifest.save(directory=directory.joinpath(repository))
