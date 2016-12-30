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

from nspawn_tools.machine import NspawnMachine, MachineNotRunningException


def _main(machine_name: str, verbose: bool=False, timeout: int=60):
    try:
        machine = NspawnMachine(machine_name)
    except MachineNotRunningException:
        if verbose:
            print("Machine '{0}' not running".format(machine))
        return

    is_running, timer = machine.stop(timeout=timeout)
    if verbose:
        if is_running:
            print("Failed to stop machine '{0}' after {1}".format(machine_name, timer), file=sys.stderr)
        else:
            print("Stopped machine '{0}' after {1}".format(machine_name, timer))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("machine_name", help="The name of the nspawn machine to gracefully terminate")
    parser.add_argument("-v", "--verbose", help="Turn on verbose output", action="store_true")
    parser.add_argument("-t", "--timeout", help="The amount of time to wait for the machine to shut down", type=int, default=60)
    args = parser.parse_args()

    try:
        _main(**args.__dict__)
    except BaseException as e:
        print("{0}: {1}".format(type(e).__name__, e), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
