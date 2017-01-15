# nspawn-tools - helper code for interacting with systemd-nspawn machines
# Copyright (C) 2016 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

import executor
from humanfriendly import Timer
import parse
from proc.unix import UnixProcess
from typing import Tuple


def find_pid(machine: str) -> int:
    cmd = executor.ExternalCommand("machinectl show {0}".format(machine), capture=True, capture_stderr=True, check=False)
    executor.execute_prepared(cmd)
    if not cmd.succeeded:
        raise MachineNotRunningException("Machine '{0}' is not running")

    results = parse.search("Leader={:d}", cmd.output)
    try:
        pid = int(results[0])
    except (ValueError, KeyError):
        raise MachineNotRunningException("Could not find PID for machine '{0}'".format(machine))
    return pid


class NspawnMachine(object):
    def __init__(self, machine: str):
        self._machine = machine
        self._process = UnixProcess(pid=find_pid(machine))

    def nsenter(self, network: bool=True, pid: bool=True):
        cmd_line = "nsenter --target {0} --mount --uts --ipc".format(self._process.pid)
        if network:
            cmd_line += " --net"
        if pid:
            cmd_line += " --pid"
        cmd = executor.ExternalCommand(cmd_line, check=False, tty=True)
        executor.execute_prepared(cmd)

    def stop(self, timeout: int=60) -> Tuple[bool, Timer]:
        stop_cmd = executor.ExternalCommand("machinectl kill {0} --kill-who=leader".format(self._machine), check=False)
        executor.execute_prepared(stop_cmd)

        timer = self._process.wait_for_process(timeout=timeout, use_spinner=False)
        return (self._process.is_running, timer)


class MachineNotRunningException(Exception):
    pass
