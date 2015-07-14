#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file LoadRTCs.py
 @brief LoadRTCs
 @date $Date$


"""
import OpenRTM_aist

import sys
import traceback
import os

import struct

import imp



def ReadString(ifs):
    s = struct.unpack("i",ifs.read(4))[0]
    a = ifs.read(s)

    return a

class RTC_FinalizeListener:
    def __init__(self, rtc, comp_list):
        self.rtc = rtc
        self.comp_list = comp_list
    def callback(self, ec_id, ret):
        print self.rtc,self.comp_list


class LoadRTCs:
    def __init__(self, mgr):
        self.mgr = mgr
        self.compList = {}

    def openFile(self):
        prop = OpenRTM_aist.Manager.instance().getConfig()
        value = ""
        value = self.getProperty(prop, "manager.modules.loadRTCs", value)
        if value != "":
            #print value
            if os.path.exists(value):
                f = open(value, 'rb')
                m = struct.unpack("i",f.read(4))[0]
                for i in range(0,m):
                    name = ReadString(f).replace("\0","")
                    d = struct.unpack("i",f.read(4))[0]
                    path = ReadString(f).replace("\0","")
                    dir = ReadString(f).replace("\0","")
                    for j in range(0,d):
                        self.createComp(name,dir)
                f.close()

    def getProperty(self, prop, key, value):
        
        if  prop.findNode(key) != None:
            #print value
            value = prop.getProperty(key)
        return value

    def createComp(self, filename, filepath):
        self.updateCompList()
        filepath = os.path.relpath(filepath)
        
        preLoadComp = None
        if self.compList.has_key(filename):
            func = self.compList[filename]["func"]
            preLoadComp = self.compList[filename]
            
        
                
                

        if preLoadComp == None:    
            func = self.getFunc(filename, filepath)
            if func == None:
                return False
            func(self.mgr)
            
        if func:
            
            comp = self.mgr.createComponent(filename)
            
            if not comp:
                return False
            
            
            if preLoadComp:
                callback_func = RTC_FinalizeListener(comp,preLoadComp)
                preLoadComp["compList"].append({"component":comp,"callback_func":callback_func})
            else:
                
                self.compList[filename] = {"filename":filename,"filepath":filepath,"func":func,"compList":[]}

                callback_func = RTC_FinalizeListener(comp,self.compList[filename])
                self.compList[filename]["compList"].append({"component":comp,"callback_func":callback_func})

            
            #comp.addPostComponentActionListener(OpenRTM_aist.PostComponentActionListenerType.POST_ON_FINALIZE, callback_func.callback)
        else:
            return False

        return True
    
        
        
    def removeComp(self, filename):
        self.updateCompList()
        if self.compList.has_key(filename):
            if len(self.compList[filename]["compList"]) != 0:
                self.compList[filename]["compList"][-1]["component"].exit()
                del self.compList[filename]["compList"][-1]
            else:
                return False
        else:
            return False
        return True
        

    def updateCompList(self):
        pass
        for i,c in self.compList.items():
            for j in c["compList"]:
                #print j.getObjRef().get_owned_contexts()
                if j["component"]._exiting:
                    c["compList"].remove(j)
                    
                
                
        

    def getCompList(self):
        import rtcControl
        self.updateCompList()
        
        names = []
        for i,c in self.compList.items():
            
            if len(c["compList"]) != 0:
                
                data = rtcControl.RTC_Data(c["filename"],len(c["compList"]))
                
                names.append(data)
            
                    
        return (True,names)

    def getFunc(self, filename, filepath):
        try:
            sys.path.append(filepath)
            (file, pathname, description) = imp.find_module(filename, [filepath])
            mod = imp.load_module(filename, file, pathname, description)
            func = getattr(mod,filename+"Init",None)

            return func
        except:
            return None

