#!/usr/bin/python3

# nspawn-tools - helper code for interacting with systemd-nspawn machines
# Copyright (C) 2016 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

import argparse
import sys

from nspawn_tools.machine import NspawnMachine


def _main(machine_name: str, no_network: bool=False, no_pid: bool=False):
    machine = NspawnMachine(machine_name)
    machine.nsenter(not no_network, not no_pid)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("machine_name", help="The name of the nspawn machine to gracefully terminate")
    parser.add_argument("-n", "--no-network", help="Don't enter the network namespace for the given machine", action="store_true")
    parser.add_argument("-p", "--no-pid", help="Don't enter the PID namespace for the given machine", action="store_true")
    args = parser.parse_args()

    try:
        _main(**args.__dict__)
    except BaseException as e:
        print("{0}: {1}".format(type(e).__name__, e), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
