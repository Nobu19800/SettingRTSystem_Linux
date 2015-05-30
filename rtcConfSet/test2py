#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file rtcConfSet.py
 @brief rtcConfSet
 @date $Date$


"""
import sys
import os
sys.path.append(".")


ba = "RTCConfData"
fname = os.path.basename(ba)
name, ext = os.path.splitext(fname)
dname = os.path.dirname(os.path.relpath(ba))

print fname
print name
print ext
print dname

print os.path.abspath("C:/Users/Nobuhiko/Desktop/DevRTC/CompositeSystem/rtcConfSet/RTCConfData2/test.txt")


dname = os.path.dirname("C:/Users/Nobuhiko/Desktop/DevRTC/CompositeSystem/rtcConfSet/RTCConfData2/test.txt")
fname = os.path.basename(dname)
if not os.path.exists(dname):
    
    os.mkdir(dname)
print dname,fname
f = open('RTCConfData2/text.txt', 'w')

f.close()
