#!/bin/bash
# /home/pi/fifostart

MYFIFO=/dev/ttyUSB20
[ -p $MYFIFO] || mkfifo $MYFIFO
