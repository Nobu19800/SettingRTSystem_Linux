#!/bin/sh
PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin
cd `dirname $0`
cmake ../../Manager/C++/rtcd_p/ -G "CodeBlocks - Unix Makefiles"
