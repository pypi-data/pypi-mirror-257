"""Utility functions to deal with the BYOA context variables"""

import configparser
from pathlib import Path
from typing import Optional

from byoa.config import DEFAULT_CONFIG_DIR

CONTEXT_FILE = "context"
REGISTRY_KEY = "registry"
ENDPOINT_KEY = "endpoint"


def get_context_value(
    key: str,
    profile="default",
    fallback: Optional[str] = None,
    config_dir: Path = DEFAULT_CONFIG_DIR,
) -> Optional[str]:
    """Get value from context file

    Args:
        key (str): Key
        profile (str, optional): Profile name. Defaults to "default".
        fallback (Optional[str], optional): Fallback value if the context value is None.
        Defaults to None.
        config_dir (Path, optional): Path to the configuration directory. Defaults to ~/.byoa

    Returns:
        str: context value
    """

    parser = configparser.ConfigParser()
    parser.read(config_dir.joinpath(CONTEXT_FILE))
    return parser.get(profile, key, fallback=fallback)


def append_context(
    registry: str, endpoint: str, profile: str, config_dir: Path = DEFAULT_CONFIG_DIR
):
    """Adds the context profile to the context file

    Args:
        registry (str): Registry value
        endpoint (str): Endpoint value
        profile (str): Profile
        config_dir (Path, optional): Path to the configuration directory. Defaults to ~/.byoa
    """

    if not config_dir.exists():
        config_dir.mkdir()

    context_file = config_dir.joinpath(CONTEXT_FILE)
    parser = configparser.ConfigParser()
    parser.read(context_file)

    if profile not in parser.sections():
        parser.add_section(profile)

    parser.set(profile, REGISTRY_KEY, registry)
    parser.set(profile, ENDPOINT_KEY, endpoint)

    with open(context_file, "w", encoding="utf-8") as f:
        parser.write(f)
