Nspawn Tools

This is a small project designed to provide helper code for interacting with
systemd-nspawn machines. At the moment, it contains two programs. Their
capabilities are described below. It also contains some associated library
code that can be used and extended for other purposes. These are designed to
work with machines that are using an init system such as runit or s6-overlay
(possibly also systemd, depending on the program).

This project is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License Version 3 as published by the Free
Software Foundation. No other version currently applies to this project. This
project is distributed without any warranty. Please see LICENSE.txt for the
full text of the license.


nspawn-enter

This is a wrapper for the nsenter utility from the util-linux package. Without
this, you would have to manually work out what the PID of the leader process
is, then run nsenter manually and remember all the flags you need to ensure you
enter all of the same namespaces that the leader process is running under.

To use nspawn-enter, run it like so:

  nspawn-enter mymachinename

It is possible to avoid entering some namespaces of the leader process. You can
pass the --no-network flag to avoid entering the network namespace. You can pass
the --no-pid flag to avoid entering the PID namespace. I added these to aid
debugging of issues within the container (especially networking issues). It can
aid things such as installing packages too. As a result, these flags are not
generic. If someone wants to provide a patch to make this generic for all
namespace flags supported by nsenter, I will be happy to consider it.


nspawn-stop

One of the problems I encountered while setting up systemd-nspawn containers
running with init systems that aren't systemd was getting the machine to shut
down cleanly when running as a systemd service unit. Initially, I was excluding
the --keep-unit flag when running systemd-nspawn in the ExecStart line of the
unit, and using 'machinectl kill mymachinename --kill-who=leader' as the
ExecStop line. Unfortunately, this still resulted in the ungraceful termination
of all processes within the container.

The ungraceful termination occurred because machinectl doesn't block until the
leader process has actually terminated. Instead, the 'machinectl kill' command
(by default) simply sends the SIGTERM signal to the leader process and then
exits immediately. Systemd would see that the ExecStop command had exited, and
that there were still processes inside the container runnng, and kill them
immediately in order to fulfill its job.

nspawn-stop gets around this issue by working out what the leader process is,
calling 'machinectl kill' itself, then waiting until the leader process has
actually terminated before exiting itself. By using this as the ExecStop
program for the relevant service unit, it gives the leader process inside the
container enough time to shut itself down cleanly.

To use nspawn-stop, run it like so:

  nspawn-stop mymachinename

It is possible to adjust the amount of time that nspawn-stop will wait for the
leader process to terminate by passing the --timeout flag:

  nspawn-stop mymachinename --timeout 10

The default timeout is 60 seconds. Note that nspawn-stop will not kill
processes inside the container itself. If the timeout expires and there are
still processes running inside the container, it is up to the caller to kill
them. When used as the ExecStop program for an nspawn machine, the caller is
systemd, and it will kill these remaining processes (as described above).
