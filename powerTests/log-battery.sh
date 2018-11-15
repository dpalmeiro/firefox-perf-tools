#!/bin/bash

rm -f battery-report.html battery-report.1.html battery-report.2.html power-log.txt

STARTTIME=`date '+%Y-%m-%d-%H_%M_%S'`
powercfg.exe /batteryreport
/mnt/c/Users/mozilla/AppData/Local/Programs/Python/Python37/python.exe parse.py
mv battery-report.html battery-report.1.html

'/mnt/c/Program Files/Intel/Power Gadget 3.5/PowerLog3.0.exe' -resolution 50 -duration 3600 -file power-log.txt

ENDTIME=`date '+%Y-%m-%d-%H_%M_%S'`
powercfg.exe /batteryreport
/mnt/c/Users/mozilla/AppData/Local/Programs/Python/Python37/python.exe parse.py
mv battery-report.html battery-report.2.html

