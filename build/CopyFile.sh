#!/bin/sh
PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin
cd `dirname $0`


cp rtcd_p/rtcd_p ../Manager/Cpp/rtcd_p/rtcd_p


copy /Y rtcdControl/src/rtcdControlComp ../rtcdControl/src/rtcdControlComp