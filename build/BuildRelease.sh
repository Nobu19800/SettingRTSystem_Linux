#!/bin/sh
PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin
script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
cd ${script_dir}
sh rtcd_p/BuildRelease.sh
sh rtcdControl/BuildRelease.sh
