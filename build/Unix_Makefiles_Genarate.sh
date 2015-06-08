#!/bin/sh
PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin
cd `dirname $0`
sh rtcd_p/Unix_Makefiles_Genarate.sh
sh rtcdControl/Unix_Makefiles_Genarate.sh
