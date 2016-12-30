#!/usr/bin/python3

# nspawn-tools - helper code for interacting with systemd-nspawn machines
# Copyright (C) 2016 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

from setuptools import find_packages, setup

from nspawn_tools import __VERSION__

setup(
    name="nspawn_tools",
    version=__VERSION__,
    license="GPLv3",
    description="Convenience code for dealing with systemd-nspawn machines",
    long_description=open("README.txt").read(),
    url="https://github.com/djmattyg007/nspawn-tools",
    author="Matthew Gamble",
    author_email="git@matthewgamble.net",
    packages=find_packages(),
    install_requires=["executor", "humanfriendly", "parse", "proc"],
    entry_points=dict(console_scripts=[
        "nspawn-enter = nspawn_tools.cli.enter:main",
        "nspawn-stop = nspawn_tools.cli.stop:main",
    ]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: System :: Systems Administration",
        "Topic :: Terminals",
        "Topic :: Utilities"
    ])
