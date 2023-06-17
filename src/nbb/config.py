import os

try:
    import tomllib as toml
except ImportError:
    import tomli as toml

from importlib.resources import files

import unicodedata


def find_config(input_cli):
    """Find the config file. the order of precedence is:
    1. cli argument
    2. environment variable
    3. ~/.config/nbb/nbb_conf.toml
    4. /etc/nbb/nbb_conf.toml
    5. default config file in the same directory as this file
    """
    if input_cli.config is not None:
        config_file = input_cli
    elif "NBB_CONF" in os.environ:
        config_file = os.environ["NBB_CONF"]
    elif os.path.exists(os.path.expanduser("~/.config/nbb/nbb_conf.toml")):
        config_file = os.path.expanduser("~/.config/nbb/nbb_conf.toml")
    elif os.path.exists("/etc/nbb/nbb_conf.toml"):
        config_file = "/etc/nbb/nbb_conf.toml"
    else:
        config_file = files("nbb").joinpath("nbb_conf.toml")
    return config_file


def get_config(config_file=None):
    """Load config file as nested dictionary."""
    if config_file is None:
        config_file = find_config(config_file)
    with open(config_file, "rb") as f:
        try:
            conf = toml.load(f)
        except FileNotFoundError:
            print(f"{config_file} specified but not found.")
            exit(1)
        except toml.TOMLDecodeError as e:
            print(e)
            exit(1)
    return conf


def normalize(config):
    """Normalize all the aliases."""

    def string_norm(string):
        return unicodedata.normalize("NFKD", string).lower()

    alias_table = {}
    for stop_name, aliases in config["stop"]["aliases"].items():
        for alias_name in aliases:
            alias_table[string_norm(alias_name)] = stop_name

        alias_table[string_norm(stop_name)] = stop_name
    return alias_table


def get_stop_infos(config, input_name):
    """Get the line code and stop area code."""
    alias_table = normalize(config)

    if input_name is not None:
        try:
            stop_name = alias_table[input_name]
        except KeyError:
            print("Provided stop name could not be map to a registered stop name.")
            exit(1)
    else:
        stop_name = list(config["stop"]["places"])[0]
    stop_code = config["stop"]["places"][stop_name]
    filters = config["stop"]["direction_filter"].get(stop_name, [])
    return stop_name, stop_code, filters
