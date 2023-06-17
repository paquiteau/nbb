# /usr/bin/env python3
"""
CLI frontend.
"""
import argparse
import datetime

from nbb.api_call import get_next_passes
from nbb.config import get_config, get_stop_infos


def parser():
    """Initialize parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=None)
    parser.add_argument("--raw", action="store_true")
    parser.add_argument("--simple", action="store_true")
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("stop_name", default=None)
    ns = parser.parse_args()
    if len(ns.stop_name) > 0:
        ns.stop_name = " ".join(ns.stop_name)
    else:
        ns.stop_name = None
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
        f"Next buses at {stop_name} planned at "
        f"{datetime.datetime.now().astimezone().strftime('%H:%M')}"
    )
    ret_string = "\n".join(
        n.as_str(ns.compact, pretty=not ns.simple) for n in next_passes if n.is_valid
    )
    print(ret_string)


if __name__ == "__main__":
    main()
