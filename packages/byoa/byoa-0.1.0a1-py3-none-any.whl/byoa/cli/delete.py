"""Delete command"""

import click
import requests
from click_option_group import RequiredMutuallyExclusiveOptionGroup, optgroup

from byoa.config.context import ENDPOINT_KEY, get_context_value
from byoa.config.manifest import Manifest
from byoa.exceptions import MissingContextValue


@click.command("delete", short_help="deletes the processor deployment")
@click.option(
    "--endpoint",
    help="BYOA API endpoint",
    envvar="BYOA_ENDPOINT",
    show_envvar=True,
    default=lambda: get_context_value(ENDPOINT_KEY),
)
@optgroup.group("Version(s)", cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option("--all", "_all", is_flag=True, help="All versions of the processor")
@optgroup.option("--version", help="Specific version")
def delete(profile: str, endpoint: str, version: str, _all: bool):
    """Dergisters the processor version

    If all versions of the processor are deregistered, the processor will be deregistered.

    Note that the version docker images will not be deleted from their registry.
    """
    if profile:
        _endpoint = get_context_value(ENDPOINT_KEY, profile, endpoint)

        if _endpoint is None:
            raise MissingContextValue(ENDPOINT_KEY)

        endpoint = _endpoint

    manifest = Manifest()

    if _all:
        click.echo("Dergister versions...", nl=False)
        response = requests.delete(
            f"{endpoint}/processors/{manifest.slug}/versions",
            timeout=60,
        )
        click.echo(response.reason)

        click.echo("Dergister processor...", nl=False)
        response = requests.delete(
            f"{endpoint}/processors/{manifest.slug}",
            timeout=60,
        )
        click.echo(response.reason)

    else:
        click.echo(f"Dergister version {version}...", nl=False)
        response = requests.delete(
            f"{endpoint}/processors/{manifest.slug}/versions/{version}",
            timeout=60,
        )
        click.echo(response.reason)
