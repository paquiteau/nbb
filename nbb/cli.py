#!/usr/bin/env python3

import argparse

from backend import request_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("line")
    parser.add_argument("stop_area")

    ns = parser.parse_args()

    data, status, errorMessage = request_data(ns.line, ns.stop_area)
    if 200 <= status < 300:
        print(data)
        # fine
    if status > 400:
        print(errorMessage)


if __name__ == "__main__":
    main()
