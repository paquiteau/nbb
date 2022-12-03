#!/usr/bin/env python3

import argparse

from backend import get_formatted_response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stop_name")
    parser.add_argument("--simple", action="store_true")
    parser.add_argument("--compact", action="store_true")
    ns = parser.parse_args()

    print(get_formatted_response(ns.stop_name, pretty=not ns.simple, compact=ns.compact))


if __name__ == "__main__":
    main()
