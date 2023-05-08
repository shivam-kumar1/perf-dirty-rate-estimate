#!/usr/bin/python
import time, os, sys
dom = sys.argv[1]
while True:
 os.system("virsh qemu-monitor-command %s '{\"execute\": \"query-migrate\"}'" % dom)
 time.sleep(0.5)
