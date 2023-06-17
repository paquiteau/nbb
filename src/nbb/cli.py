# /usr/bin/env python3
"""
CLI frontend.
"""
import argparse
import unicodedata
import os
import datetime
from pprint import pprint

try:
    import tomllib as toml
except ImportError:
    import tomli as toml

from nbb.api_call import get_next_passes


def parser():
    """Initialize parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=None)
    parser.add_argument("--raw", action="store_true")
    parser.add_argument("--simple", action="store_true")
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("stop_name", nargs="*", default=None)
    ns = parser.parse_args()
    if len(ns.stop_name) > 0:
        ns.stop_name = " ".join(ns.stop_name)
    else:
        ns.stop_name = None
    if ns.verbose:
        print("This is nbb cli\nVerbose = ON")
    return ns


def _load_toml(filename):
    with open(filename, "rb") as f:
        try:
            conf = toml.load(f)
        except FileNotFoundError:
            print(f"{filename} specified but not found.")
            exit(1)
        except toml.TOMLDecodeError as e:
            print(e)
            exit(1)
    return conf


def get_config(config_file=None):
    """Load config file."""
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), "nbb_conf.toml")

    conf = _load_toml(config_file)
    return conf


def _exit_err_msg(msg, exit_code=1):
    print(msg)
    exit(exit_code)


def string_norm(string):
    """Normalize string."""
    return unicodedata.normalize("NFKD", string).lower()


def normalize(config):
    """Normalize all the aliases."""
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
            _exit_err_msg(
                "Provided stop name could not be map to a registered stop name."
            )

    else:
        stop_name = list(config["stop"]["places"])[0]
    stop_code = config["stop"]["places"][stop_name]
    filters = config["stop"]["direction_filter"].get(stop_name, [])
    return stop_name, stop_code, filters


def main():
    """Execute main CLI function."""
    ns = parser()
    if ns.verbose:
        print("loading config")

    conf = get_config(ns.config)
    # Get the default stop as the first one registered:
    stop_name, stop_code, filters = get_stop_infos(conf, ns.stop_name)

    next_passes = get_next_passes(stop_code)
    # Remove past buses
    for i, n in enumerate(next_passes):
        if n.time < datetime.datetime.now().astimezone():
            n.is_valid = False
    # Filter by direction
    if direction_filter := conf["stop"]["direction_filter"].get(stop_name, None):
        for i, n in enumerate(next_passes):
            if n.destination not in direction_filter:
                n.is_valid = False

    print(
        f"Next buses at {stop_name} planned {datetime.datetime.now().astimezone().strftime('%H:%M')}"
    )
    ret_string = "\n".join(
        n.as_str(ns.compact, pretty=not ns.simple) for n in next_passes if n.is_valid
    )
    print(ret_string)


if __name__ == "__main__":
    main()
