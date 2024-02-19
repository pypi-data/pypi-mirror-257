"""Manifest command"""

import click

from byoa.config.manifest import Manifest, check_manifest


@click.command("manifest", short_help="sets manifest key/value pair")
@click.argument("key", type=click.Choice(Manifest.POSSIBLE_KEYS, case_sensitive=False))
@click.argument("value")
@check_manifest
def update_manifest(key: str, value: str):
    """Sets manifest KEY/VALUE pair"""

    manifest = Manifest()
    manifest.set(key, value)
    manifest.save()
