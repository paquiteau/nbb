# /usr/bin/env python3
"""
CLI frontend.
"""
import argparse
import os

try:
    import tomllib as toml
except ImportError:
    import tomli as toml

from nbb.backend import get_formatted_response


def parser():
    """Initialize parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=None)
    parser.add_argument("--simple", action="store_true")
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("stop_name", nargs="*", default=None)
    ns = parser.parse_args()
    if ns.verbose:
        print("This is nbb cli\nVerbose = ON")
    return ns


def _load_conf(filename):
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


def load_config(config_file=None):
    """Load config file."""
    if config_file is None:
        return _load_conf(os.path.join(os.path.dirname(__file__), "nbb_conf.toml"))
    return _load_conf(config_file)


def main():
    """Execute main CLI function."""
    ns = parser()
    if ns.verbose:
        print("loading config")
    conf = load_config(ns.config)

    print(
        get_formatted_response(ns.stop_name, pretty=not ns.simple, compact=ns.compact)
    )


if __name__ == "__main__":
    main()
