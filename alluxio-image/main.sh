#!/bin/bash
sudo mount -t tmpfs -o size=1g tmpfs /dev/shm
bash /alluxio/bin/alluxio-start.sh local SudoMount
