# /usr/bin/env python3
"""
CLI frontend.
"""
import argparse
import os
from pprint import pprint

try:
    import tomllib as toml
except ImportError:
    import tomli as toml

from nbb.backend import get_formatted_response, get_stop_infos, request_data


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


def main():
    """Execute main CLI function."""
    ns = parser()
    if ns.verbose:
        print("loading config")

    conf = get_config(ns.config)
    # Get the default stop as the first one registered:
    stop_name, line_code, stop_code, filters = get_stop_infos(conf, ns.stop_name)

    if ns.raw:
        data, status, error_message = request_data(line_code, stop_code)
        pprint(data)
    else:
        print(f"Next buses at {stop_name}")
        print(
            get_formatted_response(
                line_code, stop_code, filters, pretty=not ns.simple, compact=ns.compact
            )
        )


if __name__ == "__main__":
    main()
