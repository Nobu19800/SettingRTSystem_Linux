#!/bin/sh
PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin
cd `dirname $0`
sh rtcd_p/BuildDebug.sh
sh rtcdControl/BuildDebug.sh
