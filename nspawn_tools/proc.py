# nspawn-tools - helper code for interacting with systemd-nspawn machines
# Copyright (C) 2016 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

from humanfriendly import Timer
import proc.unix
import time


# TODO: Remove this once this PR has been accepted: https://github.com/xolox/python-executor/pull/3
class UnixProcess(proc.unix.UnixProcess):
    def wait_for_process(self, timeout=0, use_spinner=False):
        if use_spinner:
            return super().wait_for_process(timeout=timeout)
        timer = Timer()
        while self.is_running:
            if timeout and timer.elapsed_time >= timeout:
                break
            time.sleep(0.2)
        return timer
