# /usr/bin/env python3
"""
CLI frontend.
"""
import argparse
import datetime

from nbb.api_call import get_next_passes
from nbb.config import get_config, get_stop_infos

from nbb.models import get_message


def parser():
    """Initialize parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=None)
    parser.add_argument("--raw", action="store_true")
    parser.add_argument("--simple", action="store_true")
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("stop_name", nargs="?", default=None)
    ns = parser.parse_args()
    if ns.verbose:
        print("This is nbb cli\nVerbose = ON")
    return ns


def main():
    """Execute main CLI function."""
    ns = parser()
    if ns.verbose:
        print("loading config")

    conf = get_config(ns.config)
    # Get the default stop as the first one registered:
    print(get_message(conf, ns.stop_name, ns.simple, ns.compact))


if __name__ == "__main__":
    main()
