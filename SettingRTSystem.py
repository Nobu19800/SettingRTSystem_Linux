#!/bin/env python
# -*- encoding: utf-8 -*-

##
#   @file SettingRTCConf.py
#   @brief 



import thread



import sys,os,platform
import re
import time
import random
import commands
import math
import imp

import subprocess

import rtctree.tree

import RTC
import OpenRTM_aist

from OpenRTM_aist import CorbaNaming
from OpenRTM_aist import RTObject
from OpenRTM_aist import CorbaConsumer
from omniORB import CORBA
import CosNaming

from PyQt4 import QtCore, QtGui

import SettingRTCWindow.MainWindow






        
##
# @brief 
def main():
    #mgrc = ManagerControl("")
    
    
    if os.name == 'posix':
        process_rtcd = subprocess.Popen("python Manager/Python/rtcd.py -f Manager/Python/rtc.conf".split(" "), stdout=subprocess.PIPE)
        process_confset = subprocess.Popen("sh rtcConfSet.sh".split(" "), stdout=subprocess.PIPE)
        #process_confset = os.system("sh rtcConfSet.sh&")
    elif os.name == 'nt':
        process_rtcd = subprocess.Popen("python Manager/Python/rtcd.py -f Manager/Python/rtc.conf", stdout=subprocess.PIPE)
        process_confset = subprocess.Popen("rtcConfSet.bat", stdout=subprocess.PIPE)
        #process_confset = os.system("start rtcConfSet.bat")

            
    app = QtGui.QApplication([""])
    mainWin = SettingRTCWindow.MainWindow.MainWindow()
    mainWin.show()
    app.exec_()
    #mgrc.createComp("MyFirstComponent",[".\\MyFirstComponent"])
    #mgrc.createComp("MyFirstComponent",[".\\MyFirstComponent"])
    
    
    
    
    

    
    
    
if __name__ == "__main__":
    main()
