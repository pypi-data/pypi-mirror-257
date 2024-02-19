"""Context command"""

from pathlib import Path

import click

from byoa.config.context import (
    DEFAULT_CONFIG_DIR,
    ENDPOINT_KEY,
    REGISTRY_KEY,
    append_context,
    get_context_value,
)


@click.command("context", short_help="sets the BYOA context")
@click.option("--profile", default="default", help="Named context")
@click.option(
    "--config-dir",
    default=DEFAULT_CONFIG_DIR,
    show_default=True,
    type=Path,
    help="Context file path",
)
def context(profile: str, config_dir: Path):
    """Sets the BYOA context for deployement"""

    default_registry = get_context_value(REGISTRY_KEY, profile, config_dir=config_dir)
    default_endpoint = get_context_value(ENDPOINT_KEY, profile, config_dir=config_dir)

    registry = click.prompt("Container registry name", default_registry)
    endpoint = click.prompt("BYOA API endpoint", default_endpoint)

    append_context(registry, endpoint, profile, config_dir)
