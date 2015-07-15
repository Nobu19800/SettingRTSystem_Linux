#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file rtcConfSet.py
 @brief rtcConfSet
 @date $Date$


"""


import os.path
import traceback
import sys, traceback
import time
import struct
import subprocess
import glob

sys.path.append(".")
sys.path.append("../")

import datetime
import shutil

import rtctree.tree
import rtctree.path
import rtsprofile
import rtsprofile.rts_profile
import rtsprofile.component
import rtsprofile.config_set
import rtsprofile.exec_context
import rtsprofile.port_connectors
import rtsprofile.ports
import rtsprofile.targets

import rtshell
import rtshell.rtcryo
import rtshell.path

from SettingRTCWindow.ManagerControl import ManagerControl


# Import RTM module
import RTC
import OpenRTM_aist





import rtcconf_idl
import rtcControl_idl



import omniORB
from omniORB import CORBA, PortableServer
import RTCConfData, RTCConfData__POA
import rtcControl, rtcControl__POA


from wasanbon.core.rtc.rtcprofile import RTCProfile


def connectServicePort(obj1, obj2, c_name):

    obj1.disconnect_all()
    
    obj2.disconnect_all()

    # connect ports
    conprof = RTC.ConnectorProfile(c_name, "", [obj1,obj2], [])
    

    ret = obj2.connect(conprof)

##
#バイナリファイルより文字読み込みする関数
##
def ReadString(ifs):
    s = struct.unpack("i",ifs.read(4))[0]
    a = ifs.read(s)

    return a

##
#バイナリファイルに文字保存する関数
##
def WriteString(a, ofs):
    
    a2 = a + "\0"
    s = len(a2)
    
    d = struct.pack("i", s)
    ofs.write(d)
    
    ofs.write(a2)




def searchFile(name, dir):
    wk = os.walk(dir)
    for i in wk:
        for f in i[2]:
            if f == name:
                filepath = os.path.join(i[0],f)
                return filepath
    return ""


def getDirList(dir):
    ans = []
    files = os.listdir(dir)
    for f in files:
        path = os.path.join(dir,f)
        if os.path.isdir(path):
            ans.append(f)
    return ans



def decodestr(s):
    if isinstance(s, str):
        return s.decode('utf-8')
    return s

class RTComponentProfile():
    def __init__(self):
        self.compPath = "../Components"

    def setBasicInfo_doc(self, doc):
        reference = self.getKeyItem(doc,"rtcDoc:reference")
        license = self.getKeyItem(doc,"rtcDoc:license")
        creator = self.getKeyItem(doc,"rtcDoc:creator")
        algorithm = self.getKeyItem(doc,"rtcDoc:algorithm")
        inouts = self.getKeyItem(doc,"rtcDoc:inout")
        description = self.getKeyItem(doc,"rtcDoc:description")
        return RTCConfData.BasicInfo_Doc(reference,license,creator,algorithm,inouts,description)

    def setBasicInfo(self, rp):
        type = self.getKeyItem(rp.basicInfo,"xsi:type")
        saveProject = self.getKeyItem(rp.basicInfo,"rtcExt:saveProject")
        updateDate = self.getKeyItem(rp.basicInfo,"rtc:updateDate")
        creationDate = self.getKeyItem(rp.basicInfo,"rtc:creationDate")
        abstracts = self.getKeyItem(rp.basicInfo,"rtc:abstract")
        version = self.getKeyItem(rp.basicInfo,"rtc:version")
        vendor = self.getKeyItem(rp.basicInfo,"rtc:vendor")
        maxInstances = self.getKeyItem(rp.basicInfo,"rtc:maxInstances")
        executionType = self.getKeyItem(rp.basicInfo,"rtc:executionType")
        executionRate = self.getKeyItem(rp.basicInfo,"rtc:executionRate")
        description = self.getKeyItem(rp.basicInfo,"rtc:description")
        category = self.getKeyItem(rp.basicInfo,"rtc:category")
        componentKind = self.getKeyItem(rp.basicInfo,"rtc:componentKind")
        activityType = self.getKeyItem(rp.basicInfo,"rtc:activityType")
        componentType = self.getKeyItem(rp.basicInfo,"rtc:componentType")
        name = self.getKeyItem(rp.basicInfo,"rtc:name")
        doc = self.setBasicInfo_doc(rp.basicInfo.doc)
        return RTCConfData.BasicInfo(type,saveProject,updateDate,creationDate,abstracts,version,vendor,maxInstances,executionType,executionRate,description,category,componentKind,activityType,componentType,name,doc)
        

    def setAction(self, status):
        type = self.getKeyItem(status,"xsi:type")
        implemented = decodestr(status.implemented)

        return RTCConfData.Action(type, implemented)

    def setActions(self, rp):
        OnInitialize = self.setAction(rp.actions.OnInitialize)
        OnFinalize = self.setAction(rp.actions.OnFinalize)
        OnStartup = self.setAction(rp.actions.OnStartup)
        OnShutdown = self.setAction(rp.actions.OnShutdown)
        OnActivated = self.setAction(rp.actions.OnActivated)
        OnDeactivated = self.setAction(rp.actions.OnDeactivated)
        OnAborting = self.setAction(rp.actions.OnAborting)
        OnError = self.setAction(rp.actions.OnError)
        OnReset = self.setAction(rp.actions.OnReset)
        OnExecute = self.setAction(rp.actions.OnExecute)
        OnStateUpdate = self.setAction(rp.actions.OnStateUpdate)
        OnRateChanged = self.setAction(rp.actions.OnRateChanged)
        OnAction = self.setAction(rp.actions.OnAction)
        OnModeChanged = self.setAction(rp.actions.OnModeChanged)

        return RTCConfData.Actions(OnInitialize,OnFinalize,OnStartup,OnShutdown,OnActivated,OnDeactivated,OnAborting,OnError,OnReset,OnExecute,OnStateUpdate,OnRateChanged,OnAction,OnModeChanged)

    def setConfiguration_Doc(self, doc):
        constraint = self.getKeyItem(doc,"rtcDoc:constraint")
        range = self.getKeyItem(doc,"rtcDoc:range")
        unit = self.getKeyItem(doc,"rtcDoc:unit")
        description = self.getKeyItem(doc,"rtcDoc:description")
        defaultValue = self.getKeyItem(doc,"rtcDoc:defaultValue")
        dataname = self.getKeyItem(doc,"rtcDoc:dataname")
        return RTCConfData.Configuration_Doc(constraint,range,unit,description,defaultValue,dataname)

    def setConfiguration_Properties(self, conf):
        value = u""
        name = u""
        return RTCConfData.Configuration_Properties(value,name)

    def setConfiguration(self, conf):
        type = self.getKeyItem(conf,"xsi:type")
        variableName = self.getKeyItem(conf,"rtcExt:variableName")
        unit = self.getKeyItem(conf,"rtc:unit")
        defaultValue = self.getKeyItem(conf,"rtc:defaultValue")
        dataType = self.getKeyItem(conf,"rtc:type")
        name = self.getKeyItem(conf,"rtc:name")
        property = self.setConfiguration_Properties(conf)
        doc = self.setConfiguration_Doc(conf.doc)

        return RTCConfData.Configuration(type,variableName,unit,defaultValue,dataType,name,property,doc)

    def setDataPort_Doc(self, doc):
        operation = self.getKeyItem(doc,"rtcDoc:operation")
        occerrence = self.getKeyItem(doc,"rtcDoc:occerrence")
        unit = self.getKeyItem(doc,"rtcDoc:unit")
        semantics = self.getKeyItem(doc,"rtcDoc:semantics")
        number = self.getKeyItem(doc,"rtcDoc:number")
        type = self.getKeyItem(doc,"rtcDoc:type")
        description = self.getKeyItem(doc,"rtcDoc:description")
        return RTCConfData.DataPort_Doc(operation,occerrence,unit,semantics,number,type,description)

    def setDataPort(self, dp):
        type = self.getKeyItem(dp,"xsi:type")
        position = self.getKeyItem(dp,"rtcExt:position")
        variableName = self.getKeyItem(dp,"rtcExt:variableName")
        unit = self.getKeyItem(dp,"rtc:unit")
        subscriptionType = self.getKeyItem(dp,"rtc:subscriptionType")
        dataflowType = self.getKeyItem(dp,"rtc:dataflowType")
        interfaceType = self.getKeyItem(dp,"rtc:interfaceType")
        idlFile = self.getKeyItem(dp,"rtc:idlFile")
        datatype = self.getKeyItem(dp,"rtc:type")
        name = self.getKeyItem(dp,"rtc:name")
        portType = self.getKeyItem(dp,"rtc:portType")
        doc = self.setDataPort_Doc(dp.doc)

        return RTCConfData.DataPort(type,position,variableName,unit,subscriptionType,dataflowType,interfaceType,idlFile,datatype,name,portType,doc)

    def setServiceInterface_Doc(self, doc):
        docPostCondition = self.getKeyItem(doc,"rtcDoc:docPostCondition")
        docPreCondition = self.getKeyItem(doc,"rtcDoc:docPreCondition")
        docException = self.getKeyItem(doc,"rtcDoc:docException")
        docReturn = self.getKeyItem(doc,"rtcDoc:docReturn")
        docArgument = self.getKeyItem(doc,"rtcDoc:docArgument")
        description = self.getKeyItem(doc,"rtcDoc:description")

        return RTCConfData.ServiceInterface_Doc(docPostCondition,docPreCondition,docException,docReturn,docArgument,description)

    def setServiceInterface(self, interface):
        type = self.getKeyItem(interface,"xsi:type")
        variableName = self.getKeyItem(interface,"rtcExt:variableName")
        path = self.getKeyItem(interface,"rtc:path")
        interfeceType = self.getKeyItem(interface,"rtc:type")
        idlFile = self.getKeyItem(interface,"rtc:idlFile")
        instanceName = self.getKeyItem(interface,"rtc:instanceName")
        direction = self.getKeyItem(interface,"rtc:direction")
        name = self.getKeyItem(interface,"rtc:name")
        
        doc = self.setServiceInterface_Doc(interface.doc)

        return RTCConfData.ServiceInterface(type,variableName,path,interfeceType,idlFile,instanceName,direction,name,doc)

    def setServicePort_Doc(self, doc):
        ifdescription = self.getKeyItem(doc,"rtcDoc:ifdescription")
        description = self.getKeyItem(doc,"rtcDoc:description")
        

        return RTCConfData.ServicePort_Doc(ifdescription,description)

    def setServicePort(self, sp):
        type = self.getKeyItem(sp,"xsi:type")
        position = self.getKeyItem(sp,"rtcExt:position")
        name = self.getKeyItem(sp,"rtc:name")



        interfaces = []
        for i in sp.serviceInterfaces:
            interfaces.append(self.setServiceInterface(i))

        doc = self.setServicePort_Doc(sp.doc)

        return RTCConfData.ServicePort(type,position,name,interfaces,doc)

    def getFile(self, dirname, filename):
        filename = searchFile(filename,os.path.join(self.compPath,dirname))
        return filename
    
    def getProfile(self, name):
        filename = searchFile("RTC.xml",os.path.join(self.compPath,name))
        ans = True
        if filename != "":
            rp = RTCProfile(filename)
        else:
            rp = RTCProfile()
            ans = False
            
        info = self.setBasicInfo(rp)
        act = self.setActions(rp)
        confs = []
        if rp.configurationSet:
            for c in rp.configurationSet.configurations:
                confs.append(self.setConfiguration(c))
        dports = []
        for d in rp.getDataPorts():
            dports.append(self.setDataPort(d))
            
        sports = []

        for s in rp.serviceports:
            sports.append(self.setServicePort(s))
            
        name = decodestr(name)
        version = self.getKeyItem(rp,"rtc:version")
        id = self.getKeyItem(rp,"rtc:id")
        language = decodestr(rp.getLanguage())

        return (ans, RTCConfData.RTC_Profile(name,version,id,language,info,act,confs,dports,sports))

    def createComp(self, name):
        return True

    def removeComp(self, name):
        return True

    def getProfileList(self):
        profileList = []
        dirs = getDirList(self.compPath)
        for d in dirs:
            profile = self.getProfile(d)
            if profile[0]:
                profileList.append(profile[1])
                
        
        return (True, profileList)

    

    def getKeyItem(self, obj, key):
        
        if key in obj.keys():
            
            return decodestr(obj[key])
        return u""


    

class ConfDataInterface_i (RTCConfData__POA.ConfDataInterface):
    """
    @class ConfDataInterface_i
    Example class implementing IDL interface RTCConfData.ConfDataInterface
    """

    def __init__(self, comp):
        """
        @brief standard constructor
        Initialise member variables here
        """
        self.comp = comp
        self.confList_cpp = []
        self.confList_py = []
        self.home_dirname = ""
        self.tree = None

        self.rtcdCppFlag = False
        self.rtcdPyFlag = False

        self.rtcdControlprocess = None
        self.rtcdControlPyprocess = None

        self.filename = ""

        self.exRTCList = []

        self.runRTCList = {}        

    def open(self, filename):
        self.rtcdCppFlag = True
        self.rtcdPyFlag = True
        self.filepath = os.path.abspath(filename)
        #sys.stdout.write(filename)
        #print filename

        dirname = self.setFolder(filename)

        self.exRTCList = []
        
        #fileName = dirname[0]+"/"+dirname[1]
        fileName = os.path.join(dirname[0],dirname[1])
        #print fileName
        if os.path.exists(fileName):
            f = open(fileName, 'rb')
            m = struct.unpack("i",f.read(4))[0]
            
            for i in range(0,m):
                comp = ReadString(f).replace("\0","")
                self.exRTCList.append(comp)
            
            f.close()

        self.clean_RTCs()
        self.open_RTCs(dirname[0])

        self.setConfData_Cpp(dirname[2]+"/rtc.conf")
        self.setConfData_Py(dirname[3]+"/rtc.conf")

        if dirname[2] == "" or dirname[3] == "":
            if not os.path.exists("tmp"):
                os.mkdir("tmp")
            if not os.path.exists("tmp/Cpp"):
                os.mkdir("tmp/Cpp")
            if not os.path.exists("tmp/Python"):
                os.mkdir("tmp/Python")
            self.cppDirName = "tmp/Cpp"
            self.pyDirName = "tmp/Python"

        return True

    def setFolder(self, filename):
        if filename == "rtc.conf":
            dname = ""
            fname = "sys.conf"
            self.cppDirName = ""
            self.pyDirName = ""
        else:    
            filename = os.path.abspath(filename)
            dname = os.path.dirname(filename)
            fname = os.path.basename(filename)
            name, ext = os.path.splitext(fname)
            pname = os.path.basename(dname)
            
            if name != pname:
                
                #dname = dname + "/" + name
                dname = os.path.join(dname,name)
                if not os.path.exists(dname):
                    os.mkdir(dname)

            self.cppDirName = dname+"/Cpp"
            if not os.path.exists(self.cppDirName):
                os.mkdir(self.cppDirName)
                
            self.pyDirName = dname+"/Python"
            if not os.path.exists(self.pyDirName):
                os.mkdir(self.pyDirName)

        #print dname+"/"+fname
        self.filename = fname
        self.home_dirname = dname
        return (dname, fname, self.cppDirName, self.pyDirName)

    def getComp(self, name):
        path = ['/', 'localhost']
        nlist = name.split("/")
        for n in nlist:
            path.append(n)

        
            
        return self.tree.get_node(path)
        
    

        
        
        

    def saveConfigFile(self, comp ,filePath, rtcconffile):
        name = comp.name.split(".")[0]
        
        #compname = filePath+"/"+name+".conf"
        compname = os.path.join(filePath,name+".conf")
        f = open(compname, 'w')

        s = comp.category + "." + name + ".config_file: " + os.path.relpath(compname).replace("\\","/") + "\n"
        rtcconffile.write(s)

        s = "configuration.active_config: "
        s += str(comp.active_conf_set_name)
        s += "\n"

        f.write(s)
        
        confList = comp.conf_sets
        for k, v in confList.items():
            for i,j in v.data.items():
                s = "conf."
                s += str(k)
                s += "."
                s += str(i)
                s += ": "
                s += str(j)
                s += "\n"
                f.write(s)

        ec = comp.owned_ecs[0]
        s = "exec_cxt.periodic.rate: "
        s += str(ec.rate)
        s += "\n"

        f.write(s)

        f.close()

    def freeze_dry(self, dest='-', xml=True, abstract='', vendor='', sysname='',
        version='', components=[]):


        comp_list = []
        for c in components:
            if c.is_composite == False:
                comp_list.append(c)
        
        
        rts_components = rtshell.rtcryo.tree_comps_to_rts_comps(comp_list)
        
        data_connectors, svc_connectors = rtshell.rtcryo.find_unique_connectors(self.tree,comp_list)
        
        rtsp = rtsprofile.rts_profile.RtsProfile()
        rtsp.abstract = abstract
        today = datetime.datetime.today()
        today = today.replace(microsecond=0)
        rtsp.creation_date = today.isoformat()
        rtsp.update_date = today.isoformat()
        rtsp.version = rtsprofile.RTSPROFILE_SPEC_VERSION
        rtsp.id = 'RTSystem :{0}.{1}.{2}'.format(vendor, sysname, version)
        rtsp.components = rts_components
        rtsp.data_port_connectors = data_connectors
        rtsp.service_port_connectors = svc_connectors

        

        if dest == '-':
            
            if xml:
                sys.stdout.write(rtsp.save_to_xml())
            else:
                sys.stdout.write(rtsp.save_to_yaml())
        else:
            
            f = open(dest, 'w')
            if xml:
                f.write(rtsp.save_to_xml())
            else:
                f.write(rtsp.save_to_yaml())
            f.close()
            

    def getConnectRTCs(self, comp, clist):
        for l in clist:
            if comp.instance_name == l.instance_name:
                    return
        
        
        clist.append(comp)
        for p in comp.connected_ports:
            for c in p.connections:
                for cp in c.ports:
                    
                    if cp[1].name != p.name:
                        path = rtctree.path.parse_path(cp[0])[0]
                        cn_comp = self.tree.get_node(path)
                        
                        
                        flag = True
                        for l in clist:
                            if cn_comp.instance_name == l.instance_name:
                                flag = False
                                
                        if flag:
                            self.getConnectRTCs(cn_comp,clist)
                            #clist.append(cn_comp)

    def getDirName(self, path):
        ans = ""
        nlist = path.split("/")
        for i in range(0,len(nlist)-1):
            ans += nlist[i] + "/"



        return ans
        
        
    def getMembersName(self, comp):
        nlist = []
        for k,v in comp.members.items():
            for c in v:
                props = c.get_component_profile().properties
                for p in props:
                    if p.name == "naming.names":
                        nlist.append(p.value.value())
        return nlist
                        
    def judgeLanguage(self, comp):
        for k,v in comp.members.items():
            for c in v:
                props = c.get_component_profile().properties
                for p in props:
                    if p.name == "language":
                        if p.value.value() != "Python":
                            return "C++"
        return "Python"
    
    def judgeLanguageComps(self, comps):
        nlist = {"C++":[],"Python":[]}
        for comp in comps:
            lang = self.judgeLanguage(comp)
            nlist[lang].append(comp)
        return nlist
            
    def save(self, filename):
        filename = os.path.abspath(filename)
        self.tree = rtctree.tree.RTCTree(servers='localhost', orb=self.comp._manager.getORB())        

        compositeList = []

        mgr = self.searchMgr("manager_composite.mgr")
        if len(mgr) > 0:
            comps = mgr[0].components
            for comp in comps:
                if comp.is_composite:
                    compositeList.append(comp)
            
        compositeRTCList = self.judgeLanguageComps(compositeList)

        

        dirname = self.setFolder(filename)
        
        
        #f = open(dirname[0]+"/"+dirname[1], "wb")
        f = open(os.path.join(dirname[0],dirname[1]), "wb")
        r = len(self.exRTCList)
        d = struct.pack("i", r)
        f.write(d)

        for cn in self.exRTCList:
            WriteString(cn , f )

        f.close()

        
        f = open(dirname[2]+"/rtc.conf", 'w')
        self.saveData(f, self.confList_cpp, dirname[2], False, compositeRTCList["C++"])
        

        components = []

        cpp_path = None

        try:
            rtcs = self.comp._rtcControl_cpp._ptr().getRTC()[1]

            
            
            for n in rtcs:
                comp = self.getComp(n)
                
                if comp.name != "rtcdControl0.rtc":
                    self.getConnectRTCs(comp,components)
                    
                    self.saveConfigFile(comp, dirname[2], f)
                else:
                    cpp_path = self.getDirName(n)
            
                
        except:
            info = sys.exc_info()
            tbinfo = traceback.format_tb( info[2] )
            for tbi in tbinfo:
                print tbi


        self.save_RTCs_rtcd_cpp(f,dirname[2])
        f.close()


        f = open(dirname[3]+"/rtc.conf", 'w')
        self.saveData(f, self.confList_py, dirname[3], False, compositeRTCList["Python"])

        py_path = None

        try:
            rtcs = self.comp._rtcControl_py._ptr().getRTC()[1]

            
            
            for n in rtcs:
                comp = self.getComp(n)
                if comp.name != "rtcdControlPy0.rtc":
                    self.getConnectRTCs(comp,components)
                    self.saveConfigFile(comp, dirname[3], f)
                else:
                    py_path = self.getDirName(n)
        except:
            info = sys.exc_info()
            tbinfo = traceback.format_tb( info[2] )
            for tbi in tbinfo:
                print tbi

        self.save_RTCs_rtcd_py(f,dirname[3])
        f.close()
        
        
        self.save_RTCs(dirname[0],os.path.relpath("../workspace",dirname[0]))

        #sysFileName = dirname[0]+"/"+dirname[1].split(".")[0]+".rtsys"
        sysFileName = os.path.join(dirname[0],dirname[1].split(".")[0])+".rtsys"
        
        
        for e in self.exRTCList:
            nlist = e.split("/")
            
            del nlist[0]
            del nlist[0]
            path = ['/', 'localhost']
            path.extend(nlist)
            
            comp = self.tree.get_node(path)
            if comp:
                self.getConnectRTCs(comp,components)
        

        tmpList = compositeRTCList["C++"][:]
        tmpList.extend(compositeRTCList["Python"][:])
        for c in components:
            for t in tmpList:
                if c.name == t.name:
                    components.remove(c)
            

        

        clist = components[:]
        clist.extend(compositeRTCList["C++"])
        clist.extend(compositeRTCList["Python"])
        
        

        #dirname_home = os.path.relpath(dirname[0]).replace("\\","/")
        dirname_cpp = os.path.relpath(dirname[2]).replace("\\","/")
        dirname_py = os.path.relpath(dirname[3]).replace("\\","/")

        
        

        

        #print components
        
        if cpp_path != None and py_path != None:
            
            self.freeze_dry(sysFileName,True,"","Me","RTSystem",0,components)

            self.saveActiveFile(dirname[0],clist)
            self.saveDeactiveFile(dirname[0],clist)
            self.saveExitFile(dirname[0],clist)
            
            clist = []
            
            for c in compositeRTCList["C++"]:
                clist.append({"path":cpp_path,"comp":c})

            for c in compositeRTCList["Python"]:
                clist.append({"path":py_path,"comp":c})

            
            
            for c in components:
                if c.is_composite:
                    prop = c.properties
                    name = prop["naming.names"]
                    plist = name.split("/")
                    del plist[-1]
                    path = ""
                    
                    for n in plist:
                        path += n + "/"
                    
                    
                    if prop["language"] == "C++":
                        clist.append({"path":path,"comp":c})
                    else:
                        clist.append({"path":path,"comp":c})
                        #clist.append({"path":str(name),"comp":c})

        
            
        
            sysFileName = os.path.relpath(sysFileName,dirname[0])
            self.saveBatFile(dirname[0],dirname_cpp,dirname_py,sysFileName,clist)
        
        
        
        
        
        return True
    def saveControlRTCFile(self, home_dirname, components, filename, cmdName, allCompFlag=False):
        
        if os.name == 'posix':
            f = open(home_dirname+"/"+filename+".sh", 'w')
            
        elif os.name == 'nt':
            f = open(home_dirname+"/"+filename+".bat", 'w')
            
        self.writeFileOption(f)


        if os.name == 'nt':
            if len(components) == 0:
                f.write("rem\n")

        
                    

        for comp in components:
            #print comp.is_composite_member,comp.is_composite,comp.name
            if comp.is_composite_member == False:
                prop = comp.properties
                name = prop["naming.names"]
                path = '/localhost/'+str(name)
                if os.name == 'posix':
                    cmd = cmdName + " " + path + "\n"
                elif os.name == 'nt':
                    cmd = "cmd /c " + cmdName + " " + path + "\n"
                
                
                f.write(cmd)


        if allCompFlag:
            for comp in components:
                if comp.is_composite_member != False:        
                    prop = comp.properties
                    name = prop["naming.names"]
                    path = '/localhost/'+str(name)
                    if os.name == 'posix':
                        cmd = cmdName + " " + path + "\n"
                    elif os.name == 'nt':
                        cmd = "cmd /c " + cmdName + " " + path + "\n"
                    
                
                    f.write(cmd)


        f.close()
        
    def saveActiveFile(self, home_dirname, components):
        self.saveControlRTCFile(home_dirname,components,"active","rtact")
        
    def saveDeactiveFile(self, home_dirname, components):
        self.saveControlRTCFile(home_dirname,components,"deactive","rtdeact")
    def saveExitFile(self, home_dirname, components):
        self.saveControlRTCFile(home_dirname,components,"exit","rtexit",True)

    def writeFileOption(self, f):
        if os.name == 'posix':
            f.write("#!/bin/sh\n")
            #f.write("PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin\n")
            #f.write("script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)\n")
            #f.write("cd ${script_dir}\n")
            f.write("cd `dirname $0`\n")
        elif os.name == 'nt':
            f.write("cd /d %~dp0\n")
            
    def saveBatFile(self, home_dirname, cpp_dirname, py_dirname, sysfileName, compositeList):
        if os.name == 'posix':
            fname = home_dirname+"/start.sh"
            
            
        elif os.name == 'nt':
            fname = home_dirname+"/start.bat"
            

        if not os.path.exists(fname):
            f = open(fname, 'w')
            self.writeFileOption(f)

            shutil.copy2("../startNamingService.py", os.path.join(home_dirname,"startNamingService.py"))
            if os.name == 'posix':
                cmd = "python startNamingService.py\n"
            elif os.name == 'nt':
                cmd = "cmd /c python startNamingService.py\n"
                
            f.write(cmd)

            if os.name == 'posix':
                f.write("sh rtcStart_exe.sh\n")
            elif os.name == 'nt':
                f.write("cmd /c rtcStart_exe.bat\n")
                
            
            
            path = os.path.relpath("../workspace",home_dirname)
            if os.name == 'posix':
                path = path.replace("\\","/")
            elif os.name == 'nt':
                path = path.replace("/","\\")
                
               
            cmd = "cd " + path + "\n"
            f.write(cmd)

            
            if os.name == 'posix':
                path = "../Manager/Cpp/rtcd_p/rtcd_p".replace("\\","/")
                cmd = path + " -f " + cpp_dirname + "/rtc.conf" + "&\n"
                #cmd = "rtcd" + " -f " + cpp_dirname + "/rtc.conf" + "&\n"
            elif os.name == 'nt':
                path = "../Manager/Cpp/rtcd_p/Release/rtcd_p.exe".replace("/","\\")
                cmd = "start " + path + " -f " + cpp_dirname + "/rtc.conf" + "\n"
            f.write(cmd)

            path = "../Manager/Python/rtcd_p.py"
            if os.name == 'posix':
                path = path.replace("\\","/")
                cmd = "python " + path + " -f " + py_dirname + "/rtc.conf" + "&\n"
            elif os.name == 'nt':
                path = path.replace("/","\\")
                cmd = "start python " + path + " -f " + py_dirname + "/rtc.conf" + "\n"
            
            f.write(cmd)

            """path = os.path.relpath(home_dirname,"../workspace")
            if os.name == 'posix':
                path.replace("\\","/")
                cmd = "cd " + path + "\n"
            elif os.name == 'nt':
                path.replace("/","\\")
                cmd = "cd " + path + "\n"
            f.write(cmd)"""

            

            if os.name == 'posix':
                cmd = "cd `dirname $0`" + "\n"
            elif os.name == 'nt':
                cmd = "cd /d %~dp0" + "\n"
                    

            f.write(cmd)

            f.write("sleep 5\n")

            if os.name == 'posix':
                f.write("sh composite.sh\n")
                f.write("sh rtsystem.sh\n")

            elif os.name == 'nt':
                f.write("cmd /c composite.bat\n")
                f.write("cmd /c rtsystem.bat\n")


            f.close()

        if os.name == 'posix':
            fcomp = open(home_dirname+"/composite.sh", 'w')
        elif os.name == 'nt':
            fcomp = open(home_dirname+"/composite.bat", 'w')
            

        self.writeFileOption(fcomp)

        
        for c in compositeList:
            
            path = '/localhost/'+c["path"]+c["comp"].name

            if os.name == 'posix':
                cmd = "rtcomp " + path
            elif os.name == 'nt':
                cmd = "cmd /c rtcomp " + path
            memComp = self.getMembersName(c["comp"])

            for m in memComp:
                mempath = '/localhost/' + m
                cmd += " -a " + mempath

            cmd += "\n"
           
            fcomp.write(cmd)

            ports = c["comp"].conf_sets['default'].data['exported_ports']
            if ports != "":
                if os.name == 'posix':
                    cmd = "rtconf " + path + " set exported_ports " + ports + "\n"
                elif os.name == 'nt':
                    cmd = "cmd /c rtconf " + path + " set exported_ports " + ports + "\n"
                fcomp.write(cmd)

        fcomp.close()

        if os.name == 'posix':
            frtsystem = open(home_dirname+"/rtsystem.sh", 'w')
            self.writeFileOption(frtsystem)
            cmd = "rtresurrect " + sysfileName + "\n"
        elif os.name == 'nt':
            frtsystem = open(home_dirname+"/rtsystem.bat", 'w')
            self.writeFileOption(frtsystem)
            cmd = "cmd /c rtresurrect " + sysfileName + "\n"
            
        frtsystem.write(cmd)

        frtsystem.close()
        
        

    def getConfData(self, filename, prop, defFile):
        prop.setDefaults(OpenRTM_aist.default_config)
        
        if not os.path.exists(filename):
            fd = file(defFile,"r")
            
        else:
            fd = file(filename,"r")
            #print filename
	#print fd
        prop.load(fd)
        fd.close()

        confList = []

        for n in ManagerControl.confNameList:
                p = self.getParam(n["name"],prop)
                confList.append(RTCConfData.confData(n["name"],p))
                

        return confList

    def getDataSeq_Cpp(self):
            return (True,self.confList_cpp)

    def getDataSeq_Py(self):
            return (True,self.confList_py)
        
    # boolean getConfData(in string filename, out confDataSeq data)
    def setConfData_Cpp(self, filename):
        self.conf_filepath_cpp = filename
        self.prop_cpp  = OpenRTM_aist.Properties()
        
        self.confList_cpp = self.getConfData(self.conf_filepath_cpp, self.prop_cpp, "rtc.conf")
        
        return (True,self.confList_cpp)
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, data

    def setConfData_Py(self, filename):
        self.conf_filepath_py = filename
        self.prop_py  = OpenRTM_aist.Properties()
        
        self.confList_py = self.getConfData(self.conf_filepath_py, self.prop_py, "rtc.conf")
        
        return (True,self.confList_py)

    def getParam(self, name, prop):
        param = self.getProperty(prop, name, "")
        p = [param]
        OpenRTM_aist.StringUtil.eraseBlank(p)
        return p[0]

    
    

    ##
    #rtc.confの設定を取得する関数
    ##
    def getProperty(self, prop, key, value):
        
        if  prop.findNode(key) != None:
            
            value = prop.getProperty(key)
        return value

    def addModule_Cpp(self, filepath):
        return True
    def addModule_Py(self, filepath):
        return True
    # boolean setData(in confData data)
    def setData_Cpp(self, data):
        
        for d in range(0,len(self.confList_cpp)):
            if self.confList_cpp[d].id == data.id:
                self.confList_cpp[d] = data
                
                #return True

        
        self.confList_cpp.append(data)

        return False
        
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    def setData_Py(self, data):
        for d in range(0,len(self.confList_py)):
            if self.confList_py[d].id == data.id:
                self.confList_py[d] = data
                return True

        self.confList_cpp.append(data)
        return False

        
        #self.confList.append(data)
        
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    def getData_Cpp(self, name):
        for d in self.confList_cpp:
            if d.id == name:
                return (True, d)
        return (False,RTCConfData.confData("",""))

    def getData_Py(self, name):
        for d in self.confList_py:
            if d.id == name:
                return (True, d)
        return (False,RTCConfData.confData("",""))
    

    # boolean setDataSeq(in confDataSeq data)
    def setDataSeq_Cpp(self, data):
        self.confList_cpp = data
        return True
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    def setDataSeq_Py(self, data):
        self.confList_py = data
        return True


    def getNode(self, node, cl, ml):
        #values = node._children.values()
        values = node.children
        for v in values:
            if v.is_component:
                cl.append(v)
                        
            elif v.is_manager:
                ml.append(v)
            else:
                                    
                self.getNode(v, cl, ml)

    def getObjByName(self, name, cl):
        ans = []
        for c in cl:
            if c.name == name:
                ans.append(c)
        return ans

    def searchComp(self, name):
        self.tree = rtctree.tree.RTCTree(servers='localhost', orb=self.comp._manager.getORB())
        compList = []
        mgrList = []
        self.getNode(self.tree._root, compList, mgrList)

        return self.getObjByName(name,compList)

    def searchMgr(self, name):
        self.tree = rtctree.tree.RTCTree(servers='localhost', orb=self.comp._manager.getORB())
        compList = []
        mgrList = []
        self.getNode(self.tree._root, compList, mgrList)

        return self.getObjByName(name,mgrList)

    # boolean startRTCD()
    def startRTCD_Cpp(self):
        if not self.rtcdCppFlag:
            return False
        
        
        
        if self.rtcdControlprocess:
            self.rtcdControlprocess.kill()
            self.rtcdControlprocess = None
        
        f = open(self.cppDirName+"/rtc.conf", 'w')
        self.saveData(f, self.confList_cpp, self.cppDirName, True)
        f.close()

        if os.name == 'posix':
            com = "../rtcdControl/src/rtcdControlComp -f " + self.cppDirName.replace("\\","/") + "/rtc.conf"
            com = com.split(" ")
        elif os.name == 'nt':
            com = "../rtcdControl/src/Release/rtcdControlComp.exe -f " + self.cppDirName.replace("\\","/") + "/rtc.conf"
        
        try:
            #os.system(com)
            self.rtcdControlprocess = subprocess.Popen(com, stdout=subprocess.PIPE)
        except:
            info = sys.exc_info()
            tbinfo = traceback.format_tb( info[2] )
            for tbi in tbinfo:
                print tbi
        #os.system(com)
        
        flag = True

        while flag:
            time.sleep(0.5)
            comp = self.searchComp("rtcdControl0.rtc")
            if len(comp) > 0:
                flag = False

        
        
        comp[0].activate_in_ec(0)
        
        port = comp[0].get_port_by_name("rtcControl_cpp")

        portname = comp[0].name + "." + port.name + "." + self.comp.get_sdo_id() + "." + self.comp._rtcControl_cppPort.getName()

        connectServicePort(port.object, self.comp._rtcControl_cppPort.getPortRef(), portname)

        f = open(self.cppDirName+"/rtc.conf", 'w')
        self.saveData(f, self.confList_cpp, self.cppDirName, True)
        f.close()
        
        return True
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    def startRTCD_Py(self):
        if not self.rtcdPyFlag:
            return False

        
        
        if self.rtcdControlPyprocess:
            self.rtcdControlPyprocess.kill()
            self.rtcdControlPyprocess = None
        #self.rtcdPyFlag = True
        #print self.pyDirName+"/rtc.conf"
        f = open(self.pyDirName+"/rtc.conf", 'w')
        self.saveData(f, self.confList_py, self.pyDirName, True)
        f.close()

        if os.name == 'posix':
            com = "python ../rtcdControlPy/rtcdControlPy.py -f " + self.pyDirName.replace("\\","/") + "/rtc.conf"
            com = com.split(" ")
        elif os.name == 'nt':
            com = "python ../rtcdControlPy/rtcdControlPy.py -f " + self.pyDirName.replace("\\","/") + "/rtc.conf"
        
        #print com
        
        try:
            self.rtcdControlPyprocess = subprocess.Popen(com, stdout=subprocess.PIPE)
        except:
            info = sys.exc_info()
            tbinfo = traceback.format_tb( info[2] )
            for tbi in tbinfo:
                print tbi
        #os.system(com)
        
        flag = True

        while flag:
            time.sleep(0.5)
            comp = self.searchComp("rtcdControlPy0.rtc")
            if len(comp) > 0:
                flag = False

        
        
        comp[0].activate_in_ec(0)
        
        port = comp[0].get_port_by_name("rtcControl_py")

        portname = comp[0].name + "." + port.name + "." + self.comp.get_sdo_id() + "." + self.comp._rtcControl_pyPort.getName()

        connectServicePort(port.object, self.comp._rtcControl_pyPort.getPortRef(), portname)

        f = open(self.pyDirName+"/rtc.conf", 'w')
        self.saveData(f, self.confList_py, self.pyDirName, True)
        f.close()
        
        return True

    def saveData(self, fd, confList, filepath,  rtcdFlag=True,compositeList=[]):
        
        for d in confList:
            s = d.id + ": "

            
            
            if d.id == "manager.components.precreate":
                
                for c in range(0,len(compositeList)):
                    s += "PeriodicECSharedComposite?&instance_name="+compositeList[c].name.split(".")[0]
                    #print c.name.split(".")
                    if c != len(compositeList)-1:
                        s += ","

                if d.data != "":
                     s += ","
                        
            if rtcdFlag and d.id == "exec_cxt.periodic.type":
                s += "PeriodicExecutionContext"
            
            elif rtcdFlag == False and d.id == "exec_cxt.periodic.filename" and d.data == "":
                text = os.path.relpath(filepath).replace("\\","/") + "/order.conf"
                
                of = open(text, "wb")
                of.close()
                s += text
                
            else:
                s += d.data
                
                    
            s += "\n"

        
            
            fd.write(s)

        filename = os.path.join(filepath,"RTCs_rtcd.conf")
        filename = os.path.relpath(filename)
        if os.path.exists(filename):
            filename = filename.replace("\\","/")
            #print "manager.modules.loadRTCs: "+filename+"\n"
            fd.write("manager.modules.loadRTCs: "+filename+"\n")

    # boolean exitRTCD()
    def exitRTCD_Cpp(self):
        
        return True
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    def exitRTCD_Py(self):
        
        return True

    def getRelPath(self, filepath):
        return os.path.relpath(filepath).replace("\\","/")

    def setSystem(self):
        if os.name == 'posix':
            name = self.home_dirname+"/composite.sh"
            com = os.path.relpath(name).replace("\\","/")
            com = "sh " + com
            com = com.split(" ")
        elif os.name == 'nt':
            name = self.home_dirname+"/composite.bat"
            com = os.path.relpath(name).replace("/","\\")
            
        if os.path.exists(name):
            
                
            
            time.sleep(5)
            
            
            try:
                process = subprocess.Popen(com, stdout=subprocess.PIPE)
            except:
                info = sys.exc_info()
                tbinfo = traceback.format_tb( info[2] )
                for tbi in tbinfo:
                    print tbi
            #os.system(com)
            
        #name = self.home_dirname+"/rtsystem.bat"
        name = self.home_dirname + "/" + self.filename.split(".")[0]+".rtsys"
        if os.path.exists(name):
            if os.name == 'posix':
                com = "rtresurrect " + os.path.relpath(name).replace("\\","/")
                com = com.split(" ")
            elif os.name == 'nt':
                com = "cmd /c rtresurrect " + os.path.relpath(name).replace("\\","/")
            
            try:
                process = subprocess.Popen(com, stdout=subprocess.PIPE)
            except:
                info = sys.exc_info()
                tbinfo = traceback.format_tb( info[2] )
                for tbi in tbinfo:
                    print tbi
            #os.system(com)
        
        return True

    def setExRTCList(self, name):
        self.exRTCList = name[:]
        #print self.exRTCList
        return True
    def getExRTCList(self):
        return (True,self.exRTCList)

    def createNonExistFolder(self, path):
        #filename = os.path.abspath(path)
        #dname = os.path.dirname(filename)
        #fname = os.path.basename(filename)
        #name, ext = os.path.splitext(fname)
        #pname = os.path.basename(dname)
        
        dnameList = os.path.relpath(path).replace("\\","/").split("/")

        epath = "./"
        for d in dnameList:
            epath = os.path.join(epath, d)
            if not os.path.exists(epath):
                
                os.mkdir(epath)
        

    def saveDir(self, path, filepath):
        
        path.replace("\\","/")
        if path == "./" or path == ".":
            return
        p = os.path.relpath(path,"../").replace("\\","/")
        
        
        plist = p.split("/")
        if plist[0] == "..":
            return

        p2 = os.path.relpath(path, self.home_dirname).replace("\\","/")
        plist = p2.split("/")
        
        if plist[0] != "..":
            return
        
        filename = os.path.abspath(filepath)
        dname = os.path.dirname(filename)

        
        fn = os.path.join(dname,p)
        
        self.createNonExistFolder(os.path.join(fn,"../"))

        
        if os.path.exists(fn):
            shutil.rmtree(fn)
        shutil.copytree(path, fn)
        
    def getUseDll(self, root, filename):
        nameList = []
        for name in glob.glob(os.path.join(root,filename)):
            nameList.append(name)
        return nameList


    def createDirectDirScript(self, name, dname, homedir_fp):
        sname = os.path.join(dname,name)
            
        if os.name == 'posix':
            fname = sname+".sh"
            if os.path.exists(fname):
                return
            f = open(fname, 'w')
            self.writeFileOption(f)
            com = os.path.join(homedir_fp,name) + ".sh"
            com = "sh " + com.replace("\\","/")
            f.write(com)
            
        elif os.name == 'nt':
            fname = sname+".bat"
            if os.path.exists(fname):
                return
            f = open(fname, 'w')
            self.writeFileOption(f)
            com = com = os.path.join(homedir_fp,name) + ".bat"
            com = "cmd /c " + com.replace("/","\\")
            f.write(com)
        

        f.close()

    def createProject(self, filepath):
        if not self.rtcdCppFlag:
            return False
        if not self.rtcdPyFlag:
            return False
        

        filename = os.path.abspath(filepath)
        dname = os.path.dirname(filename)
        fname = os.path.basename(filename)
        name, ext = os.path.splitext(fname)
        pname = os.path.basename(dname)

        
        if name != pname:
            dname = os.path.join(dname,name)
            #dname = dname + "/" + name
            if not os.path.exists(dname):
                os.mkdir(dname)
        

        f = open(os.path.join(dname,fname), 'w')
        f.close()


        path_list = []
        for c in self.confList_cpp:
            if c.id == "manager.modules.load_path":
                l = c.data.split(",")
                for i in l:
                    path_list.append(i)
        for c in self.confList_py:
            if c.id == "manager.modules.load_path":
                l = c.data.split(",")
                for i in l:
                    path_list.append(i)

        for l in path_list:
            self.saveDir(l,os.path.join(dname,fname))

        homedir_fp = os.path.relpath(self.home_dirname,"../")
        fn = os.path.join(dname,os.path.relpath(homedir_fp))
        
        self.createNonExistFolder(os.path.join(fn,"../"))

        if os.path.exists(fn):
            shutil.rmtree(fn)
        shutil.copytree(self.home_dirname, fn)

        manager_fn = os.path.join(dname,"Manager")
        if os.path.exists(manager_fn):
            shutil.rmtree(manager_fn)
        shutil.copytree("../Manager", manager_fn)

        wp = os.path.join(dname,"workspace")
        if not os.path.exists(wp):
            os.mkdir(wp)

        cp = os.path.join(dname,"Components")
        if not os.path.exists(cp):
            os.mkdir(cp)

        try:
            ans, rtc_list = self.comp._rtcControl_cpp._ptr().getCompList()
            self.copyRTComponentDir(rtc_list,cp)
            ans, rtc_list = self.comp._rtcControl_py._ptr().getCompList()
            self.copyRTComponentDir(rtc_list,cp)
        except:
            info = sys.exc_info()
            tbinfo = traceback.format_tb( info[2] )
            for tbi in tbinfo:
                print tbi
        

        if os.name == 'nt':
            omni_root = os.environ.get("OMNI_ROOT")
            rtm_root = os.environ.get("RTM_ROOT")
            dlist = []
            if omni_root:
                pl = self.getUseDll(omni_root,"bin/*/omniDynamic*.dll")
                dlist.extend(pl[:])
                pl = self.getUseDll(omni_root,"bin/*/omnithread*.dll")
                dlist.extend(pl[:])
                pl = self.getUseDll(omni_root,"bin/*/omniORB*.dll")
                dlist.extend(pl[:])
            if rtm_root:
                pl = self.getUseDll(rtm_root,"bin/coil*.dll")
                dlist.extend(pl[:])
                pl = self.getUseDll(rtm_root,"bin/RTC*.dll")
                dlist.extend(pl[:])

            for d in dlist:
                d_fname = os.path.basename(d)
                cpp_manager_fn = os.path.join(manager_fn,"Cpp/rtcd_p/Release")
                shutil.copy2(d, os.path.join(cpp_manager_fn,d_fname))

        
            
        self.createDirectDirScript("start", dname, homedir_fp)
        self.createDirectDirScript("active", dname, homedir_fp)
        self.createDirectDirScript("deactive", dname, homedir_fp)
        self.createDirectDirScript("exit", dname, homedir_fp)
        """homedir_fp
        f = open(os.path.join(dname,fname), 'w')
        """
        #print self.home_dirname
        #print path_list
        #self.confList_cpp = []
        #self.confList_py = []
        return True

    def copyRTComponentDir(self, rtc_list, dir):
        for c in rtc_list:
            if c.num != 0:
                path1 = os.path.join("../Components",c.name)
                path2 = os.path.join(dir,c.name)
                if os.path.exists(path1):
                    shutil.copytree(path1, path2)

    def getProfile(self, name):
        rp = RTComponentProfile()

        return rp.getProfile(name)

    """def getRTC_Num(self, lobj):
        count = 0
        while True:
            if str(count) not in lobj:
                return str(count)
            count += 1"""
        
    def updateCompList(self):
        for k,v in self.runRTCList.items():
            for c in v:
                if c["type"] == 1:
                    if c["process"].poll() != None:
                        v.remove(c)

    def getFilePath_dll(self, name):
        rp = RTComponentProfile()
        filename = name
        if os.name == 'posix':
            filename += ".so"
        elif os.name == 'nt':
            filename += ".dll"
        filepath = rp.getFile(name, filename)
        if filepath != "":
            path = os.path.relpath(filepath)
            dname = os.path.dirname(path)
            return path,dname
        return "",""

    def getFilePath_exe(self, name):
        rp = RTComponentProfile()
        filename = name + "Comp"
        if os.name == 'nt':
            filename += ".exe"
        filepath = rp.getFile(name, filename)
        if filepath != "":
            path = os.path.relpath(filepath)
            dname = os.path.dirname(path)
            bname = os.path.basename(path)
            return path,dname,bname
        return "","",""

    def getFilePath_py(self, name):
        rp = RTComponentProfile()
        filename = name
        filename += ".py"
        filepath = rp.getFile(name, filename)
        if filepath != "":
            path = os.path.relpath(filepath)
            dname = os.path.dirname(path)
            bname = os.path.basename(path)
            return path,dname,bname
        return "","",""

    def createComp(self, name, runtype):
        self.updateCompList()
        rp = RTComponentProfile()
        ans,profile = rp.getProfile(name)
        
        if ans:
            if runtype == 0:
                if profile.language == u"C++":
                    
                    path,dname = self.getFilePath_dll(name)

                    if path != "":
                        #if len(self.comp._rtcControl_cppPort.get_connector_profiles()) > 0:
                        try:
                            ans = self.comp._rtcControl_cpp._ptr().createComp(name,dname)
                        except:
                            return False
                            #ans = self._rtcControl_cpp._ptr().createComp("MyFirstComponent","..\\..\\..\\..\\Components\\MyFirstComponent\\src\\Release")
                            
                        if name not in self.runRTCList:
                            self.runRTCList[name] = []
                        #num = self.getRTC_Num(self.runRTCList[name])
                        #self.runRTCList[name][num] = {"type":runtype,"language":profile.language}
                        self.runRTCList[name].append({"type":runtype,"language":profile.language,"directory":dname})
                                
                        return True
                        
                    else:
                        return False
                elif profile.language == u"Python":
                    
                    path,dname,bname = self.getFilePath_py(name)

                    if path != "":
                        try:
                            ans = self.comp._rtcControl_py._ptr().createComp(name,dname)
                        except:
                            return False

                        if name not in self.runRTCList:
                            self.runRTCList[name] = []
                        #num = self.getRTC_Num(self.runRTCList[name])
                        #self.runRTCList[name][num] = {"type":runtype,"language":profile.language}
                        self.runRTCList[name].append({"type":runtype,"language":profile.language,"directory":dname})
                                
                        return True

                    else:
                        return False
            else:
                if name in self.runRTCList:
                    if len(self.runRTCList) > 0:
                        
                        return False
                    
                if profile.language == u"C++":
                    
                    path,dname,bname = self.getFilePath_exe(name)

                    if path != "":
                        com = bname

                        if os.name == 'posix':
                            com = com.split(" ")
                        
                        cwd = os.getcwd()
                        os.chdir(dname)
                        
                        sp = subprocess.Popen(com, stdout=subprocess.PIPE)
                        os.chdir(cwd)
                        
                        if name not in self.runRTCList:
                            
                            self.runRTCList[name] = []
                            
                        #num = self.getRTC_Num(self.runRTCList[name])
                        
                        #self.runRTCList[name][num] = {"type":runtype,"process":sp,"language":profile.language}
                        self.runRTCList[name].append({"type":runtype,"process":sp,"language":profile.language,"directory":dname,"filename":bname})
                            
                        return True
                    else:
                        return False
                    
                elif profile.language == u"Python":
                    path,dname,bname = self.getFilePath_py(name)

                    if path != "":
                        com = "python " + bname
                        if os.name == 'posix':
                            com = com.split(" ")
                        
                        cwd = os.getcwd()
                        os.chdir(dname)
                        sp = subprocess.Popen(com, stdout=subprocess.PIPE)
                        os.chdir(cwd)

                        if name not in self.runRTCList:
                            self.runRTCList[name] = []
                        #num = self.getRTC_Num(self.runRTCList[name])
                        #self.runRTCList[name][num] = {"type":runtype,"process":sp,"language":profile.language}
                        self.runRTCList[name].append({"type":runtype,"process":sp,"language":profile.language,"directory":dname,"filename":bname})
                        return True
                    else:
                        return False
                    
                
        return False

    def removeComp(self, name):
        """self.updateCompList()
        if name in self.runRTCList:
            
            if id in self.runRTCList[name]:
                
                if id in self.runRTCList[name]:
                    
                    if self.runRTCList[name][id]["type"] == 0:
                        ans = False
                        language = self.runRTCList[name][id]["language"]
                        if language == u"C++":
                            if len(self.comp._rtcControl_cppPort.get_connector_profiles()) > 0:
                                ans = self.comp._rtcControl_cpp._ptr().removeComp(name)
                        elif language == u"Python":
                            if len(self.comp._rtcControl_pyPort.get_connector_profiles()) > 0:
                                ans = self.comp._rtcControl_py._ptr().removeComp(name)
                                
                        if ans:
                            del self.runRTCList[name][id]
                            return True
                    else:
                        
                        self.runRTCList[name][id]["process"].kill()
                        
                        del self.runRTCList[name][id]
                        return True
        """            
        return False

    def getProfileList(self):
        
        rp = RTComponentProfile()
        
        return rp.getProfileList()

    def saveRTCsData(self, filename, rtc_list, mode):
        
        f = open(filename, "wb")
        
        r = len(rtc_list)
        d = struct.pack("i", r)
        f.write(d)
        
        for c in rtc_list:
            
            WriteString(c["name"],f)
            d = struct.pack("i", c["num"])
            
            f.write(d)
            if mode == 0:
                WriteString(c["path"],f)
                
                WriteString(c["directory"],f)
                
                
            
            
            
        
        f.close()

    def save_RTCs_rtcd_cpp(self, confFile, path):
        try:
            
            ans, rtc_list = self.comp._rtcControl_cpp._ptr().getCompList()
            c_list = []
            
            for c in rtc_list:
                if c.num != 0:
                    fname,dname = self.getFilePath_dll(c.name)
                    c_list.append({"name":c.name,"num":c.num,"language":"C++","path":fname,"directory":dname})
                
            filename = os.path.join(path,"RTCs_rtcd.conf")
            
            filename = filename.replace("\\","/")
            
                
            confFile.write("manager.modules.loadRTCs: "+filename+"\n")

            self.saveRTCsData(filename, c_list, 0)
            
        except:
            info = sys.exc_info()
            tbinfo = traceback.format_tb( info[2] )
            for tbi in tbinfo:
                print tbi
                
    def save_RTCs_rtcd_py(self, confFile, path):
        try:
            ans, rtc_list = self.comp._rtcControl_py._ptr().getCompList()
            
            c_list = []
            
            for c in rtc_list:
                if c.num != 0:
                    fname,dname,bname = self.getFilePath_py(c.name)
                    c_list.append({"name":c.name,"num":c.num,"language":"Python","path":fname,"directory":dname})

            filename = os.path.join(path,"RTCs_rtcd.conf")
            
            filename = filename.replace("\\","/")
            
                
            confFile.write("manager.modules.loadRTCs: "+filename+"\n")
            
            self.saveRTCsData(filename, c_list, 0)
        except:
            info = sys.exc_info()
            tbinfo = traceback.format_tb( info[2] )
            for tbi in tbinfo:
                print tbi
                
    def open_RTCs(self, path):
        filename = os.path.join(path,"RTCs.conf")
        
        if os.path.exists(filename):
            f = open(filename, 'rb')
            m = struct.unpack("i",f.read(4))[0]
            for i in range(0,m):
                name = ReadString(f).replace("\0","")
                num = struct.unpack("i",f.read(4))[0]
                for n in range(0,num):
                    self.createComp(name, 1)
            f.close()

    def clean_RTCs(self):
        for k,v in self.runRTCList.items():
            for c in v:
                if c["type"] == 0:
                    pass
                else:
                    c["process"].kill()
        self.runRTCList = {}
        
    def save_RTCs(self, path, workspace):
        
        rtc_list = []
        batfile = os.path.join(path, "rtcStart_exe")
        if os.name == 'posix':
            f = open(batfile+".sh", 'w')
            
        elif os.name == 'nt':
            f = open(batfile+".bat", 'w')
            
        self.writeFileOption(f)

        

        if os.name == 'posix':
            workspace = workspace.replace("\\","/")
        elif os.name == 'nt':
            workspace = workspace.replace("/","\\")
                
               
        cmd = "cd " + workspace + "\n"
        f.write(cmd)
        
        #print self.runRTCList
        for k,v in self.runRTCList.items():
            if len(v) != 0:
                if v[0]["type"] != 0:
                    data = {"name":k,"num":len(v)}
                    
                    rtc_list.append(data)

                    if os.name == 'posix':
                        cmd = "cd " + v[0]["directory"].replace("\\","/") + "\n"
                    elif os.name == 'nt':
                        cmd = "cd " + v[0]["directory"].replace("/","\\") + "\n"

                    f.write(cmd)

                    cmd_sub = ""
                    if v[0]["language"] == u"Python":
                        cmd_sub = "python "

                    if os.name == 'posix':
                        cmd = "start " + cmd_sub + v[0]["filename"] + "\n"
                    elif os.name == 'nt':
                        cmd = "start " + cmd_sub + v[0]["filename"] + "\n"

                    f.write(cmd)

                    if os.name == 'posix':
                        cmd = "cd `dirname $0`" + "\n"
                    elif os.name == 'nt':
                        cmd = "cd /d %~dp0" + "\n"
                    

                    f.write(cmd)

                    cmd = "cd " + workspace + "\n"
                    f.write(cmd)
                
            #data = rtcControl.RTC_Data(k, len(v))
            #rtc_list.append(data)

        if len(rtc_list) == 0:
            if os.name == 'nt':
                f.write("rem\n")
                
        f.close()
        
        self.saveRTCsData(os.path.join(path,"RTCs.conf"), rtc_list, 1)

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
rtcconfset_spec = ["implementation_id", "rtcConfSet", 
		 "type_name",         "rtcConfSet", 
		 "description",       "rtcConfSet", 
		 "version",           "1.0.0", 
		 "vendor",            "Miyamoto Nobuhiko", 
		 "category",          "TES", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class rtcConfSet
# @brief rtcConfSet
# 
# 
class rtcConfSet(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
                self._manager = manager
		"""
		"""
		self._rtcconfPort = OpenRTM_aist.CorbaPort("rtcconf")
		"""
		"""
		self._rtcControl_cppPort = OpenRTM_aist.CorbaPort("rtcControl_cpp")
		"""
		"""
		self._rtcControl_pyPort = OpenRTM_aist.CorbaPort("rtcControl_py")

		"""
		"""
		self._rtcconf = ConfDataInterface_i(self)
		
		#self._rtcconf.createComp("MySecondComponent",1)

		#print self._rtcconf.getProfileList()
		#print self._rtcconf.getProfile("MyFirstComponent")

        

		"""
		"""
		self._rtcControl_cpp = OpenRTM_aist.CorbaConsumer(interfaceType=rtcControl.RTCDataInterface)
		"""
		"""
		self._rtcControl_py = OpenRTM_aist.CorbaConsumer(interfaceType=rtcControl.RTCDataInterface)

		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		self._rtcconfPort.registerProvider("rtcconf", "RTCConfData::ConfDataInterface", self._rtcconf)
		
		# Set service consumers to Ports
		self._rtcControl_cppPort.registerConsumer("rtcControl_cpp", "rtcControl::RTCDataInterface", self._rtcControl_cpp)
		self._rtcControl_pyPort.registerConsumer("rtcControl_py", "rtcControl::RTCDataInterface", self._rtcControl_py)
		
		# Set CORBA Service Ports
		self.addPort(self._rtcconfPort)
		self.addPort(self._rtcControl_cppPort)
		self.addPort(self._rtcControl_pyPort)
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
                try:
                    pass
                    #self._rtcconf.open_RTCs(".")
                    #self._rtcconf.createComp("MySecondComponent",0)
                    #self._rtcconf.createComp("MySecondComponent",0)
                    #self._rtcconf.createComp("MySecondComponent",0)
                    
                except:
                    info = sys.exc_info()
                    tbinfo = traceback.format_tb( info[2] )
                    for tbi in tbinfo:
                        print tbi
                #self._rtcconf.createComp("MySecondComponent",1)
                #self._rtcconf.createComp("MySecondComponent",1)
                
                #print self._rtcControl_cpp._ptr().createComp("MyFirstComponent","..\\..\\..\\..\\Components\\MyFirstComponent\\src\\Release")
                #print self._rtcControl_py._ptr().createComp("MySecondComponent","..\\Components\\MySecondComponent")
                
		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
                try:
                    pass
                    #print self._rtcControl_py._ptr().getCompList()
                    #self._rtcconf.save_RTCs(None,".")
                    #self._rtcconf.save_RTCs(".",".")
                    #self._rtcconf.clean_RTCs()
                    #f = open("test2.conf", "w")
                    #self._rtcconf.save_RTCs_rtcd_py(f,".")
                    #f.close()
                except:
                    info = sys.exc_info()
                    tbinfo = traceback.format_tb( info[2] )
                    for tbi in tbinfo:
                        print tbi
                #self._rtcconf.updateCompList()
                #print  self._rtcconf.runRTCList
                #self._rtcconf.removeComp("MySecondComponent","2")
                #print self._rtcconf.runRTCList
                #print self._rtcControl_py._ptr().getCompList()
                #print self._rtcControl_cpp._ptr().removeComp("MyFirstComponent")
                #print self._rtcControl_py._ptr().removeComp("MySecondComponent")
                #print self._rtcControl_py._ptr().getCompList()
		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):

        	
                #print len(self._rtcControl_pyPort.get_connector_profiles())

        
        
        
        # *** Implement me
        # Must return: result, data
        #self._rtcconf.save("")
        #print self._rtcControl_py._ptr().getRTC()
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def rtcConfSetInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=rtcconfset_spec)
    manager.registerFactory(profile,
                            rtcConfSet,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    rtcConfSetInit(manager)

    # Create a component
    comp = manager.createComponent("rtcConfSet")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

