#!usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from battery_notify.daemon import BatteryDaemon


def run_app() -> None:
    """ Run the battery-notify app. """
    bat_daemon = BatteryDaemon()
    args: list = sys.argv
    args.pop(0)
    bat_daemon.run(args)
