#!/bin/env python
# -*- encoding: utf-8 -*-

##
#   @file .py
#   @brief 



import thread


import optparse
import sys,os,platform
import traceback
import re
import time
import random
import commands
import math
import imp

import rtctree.tree

import RTC
import OpenRTM_aist

from OpenRTM_aist import CorbaNaming
from OpenRTM_aist import RTObject
from OpenRTM_aist import CorbaConsumer
from omniORB import CORBA
import CosNaming

from PyQt4 import QtCore, QtGui



from SettingRTCConf.ConfigWidget import ConfigWidget
from SettingRTCConf.CorbaWidget import CorbaWidget
from SettingRTCConf.ExecCxtWidget import ExecCxtWidget
from SettingRTCConf.LoggerWidget import LoggerWidget

from SettingRTCConf.ManagerWidget import ManagerWidget
from SettingRTCConf.NamingWidget import NamingWidget
from SettingRTCConf.TimerWidget import TimerWidget

from SettingRTCWindow.TabWidget import TabWidget
from SettingRTCWindow.ManagerControl import ManagerControl

from SettingRTCWindow.rtcdWidget import rtcdWidget

import imp



def connectServicePort(obj1, obj2, c_name):

    

    obj1.disconnect_all()
    
    obj2.disconnect_all()

    # connect ports
    conprof = RTC.ConnectorProfile(c_name, "", [obj1,obj2], [])

    

    ret = obj2.connect(conprof)

    



class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

	self.setWindowTitle(u"複合コンポーネント作成支援ツール")
        self.tree = None
        
        self.mgr = OpenRTM_aist.Manager.init(sys.argv)
        
        self.mgr.activateManager()
        self.mgr.runManager(True)


        filename = "rtcConfSetReq"
	filepath = ["./rtcConfSetReq"]
	func = self.getFunc(filename, filepath)
	func(self.mgr)
        self.control_comp = self.mgr.createComponent(filename)

        

        

        self.tab_widget = QtGui.QTabWidget(self)
        self.rtcd_widget = rtcdWidget(self)

        self.tab_widget.addTab(self.rtcd_widget, u"RTCD")
        
        self.setCentralWidget(self.tab_widget)

        self.createAction()
	self.createMenus()

	#self.mgrc = ManagerControl("")
	
	self.tab_widget_cpp =  None
	self.tab_widget_python = None


	
	self.curFile = ""

	#self.mgrc.CreateComp("MyFirstComponent",[".\\MyFirstComponent"])
        #self.mgrc.CreateComp("MyFirstComponent",[".\\MyFirstComponent"])


    def searchRTC(self, name, ip='localhost'):
        ans = []
        
        self.tree = rtctree.tree.RTCTree(servers=ip, orb=self.control_comp._manager.getORB())
        node = self.tree._root
        
        compList = []
        self.getNode(node, compList)

        for c in compList:
            if c.name == name:
                ans.append(c)

        

        return ans


    def getNode(self, node, cl):
        values = node._children.values()
        for v in values:
            if v.is_component:
                cl.append(v)
                    
            elif v.is_manager:
                pass
            else:
                                
                self.getNode(v, cl)
        
    ##
    #アクションの作成の関数
    ##
    def createAction(self):

	self.newAct = QtGui.QAction("&New...",self)
	self.newAct.setShortcuts(QtGui.QKeySequence.New)
        self.newAct.triggered.connect(self.newFile)
        


	self.openAct = QtGui.QAction("&Open...",self)
        self.openAct.setShortcuts(QtGui.QKeySequence.Open)
        self.openAct.triggered.connect(self.open)


        self.saveAct = QtGui.QAction("&Save",self)
        self.saveAct.setShortcuts(QtGui.QKeySequence.Save)
        self.saveAct.triggered.connect(self.save)

        self.saveAsAct = QtGui.QAction("&Save &As",self)
        self.saveAsAct.setShortcuts(QtGui.QKeySequence.SaveAs)
        self.saveAsAct.triggered.connect(self.saveAs)

    def deleteTabs(self):
        if self.tab_widget_cpp:
            self.tab_widget.removeTab(self.tab_widget.indexOf(self.tab_widget_cpp))
            self.tab_widget_cpp = None
        if self.tab_widget_python:
            self.tab_widget.removeTab(self.tab_widget.indexOf(self.tab_widget_python))
            self.tab_widget_python = None
    ##
    #メニューの作成の関数
    ##
    def createMenus(self):

	self.fileMenu = self.menuBar().addMenu("&File")
	self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)


    def createTabs(self, filapath):
        ipaddress = str(self.rtcd_widget.WidList["textBox"]["Widget"].text().toLocal8Bit())
        confsetComp = self.searchRTC("rtcConfSet0.rtc",ipaddress)
        confsetPort = confsetComp[0].get_port_by_name("rtcconf")
        #print confsetPort

        confsetComp[0].activate_in_ec(0)
        portname = confsetComp[0].name + "." + confsetPort.name + "." + self.control_comp.get_sdo_id() + "." + self.control_comp._rtcconfPort.getName()
        
        connectServicePort(confsetPort.object, self.control_comp._rtcconfPort.getPortRef(), portname)

        

        self.control_comp.get_owned_contexts()[0].activate_component(self.control_comp.getObjRef())


        self.mgrc_cpp = ManagerControl(filapath,self.control_comp,ManagerControl.CPP)
        self.mgrc_py = ManagerControl(filapath,self.control_comp,ManagerControl.PY)

        flag = True

        while flag:
            
            try:
                self.control_comp._rtcconf._ptr().open(filapath)
                wid = self.rtcd_widget.WidList["rtcList"]["Widget"]
                clist = self.control_comp._rtcconf._ptr().getExRTCList()[1]
                wid.clear()
                for c in clist:
                    wid.addItem(c)
                
                flag = False
            except:
                info = sys.exc_info()
                tbinfo = traceback.format_tb( info[2] )
                for tbi in tbinfo:
                    print tbi

        self.mgrc_cpp.SetParam()
        self.mgrc_py.SetParam()


        self.deleteTabs()

        if self.tab_widget_cpp == None:
            self.tab_widget_cpp = TabWidget(self.mgrc_cpp,"C++")
            self.tab_widget.addTab(self.tab_widget_cpp, u"CPP")

        if self.tab_widget_python == None:
            self.tab_widget_python = TabWidget(self.mgrc_py,"Python")
            self.tab_widget.addTab(self.tab_widget_python, u"Python")
        
        

    def getFunc(self, filename, filepath):
        try:
            sys.path.append(filepath[0])
            (file, pathname, description) = imp.find_module(filename, filepath)
            mod = imp.load_module(filename, file, pathname, description)
            func = getattr(mod,filename+"Init",None)

            return func
        except:
            info = sys.exc_info()
            tbinfo = traceback.format_tb( info[2] )
            for tbi in tbinfo:
                print tbi
            return None

    def getFilePath(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","","Config File (*.conf);;All Files (*)")
        if fileName.isEmpty():
            return ""
        ba = str(fileName.toLocal8Bit())
        #ba = ba.replace("/","\\")
        

        return ba

    ##
    #ファイル読み込みスロット
    ##
    def open(self):
        
        

        filepath = self.getFilePath()
        if filepath == "":
            return

        self.createTabs(filepath)
        self.curFile = filepath
        
        
        
    def setDataCpp(self):
        if self.tab_widget_cpp !=  None:
            data = self.tab_widget_cpp.getConfData() 
            cdata = self.control_comp.convConfData(data)
            try:
                self.control_comp._rtcconf._ptr().setDataSeq_Cpp(cdata)
            except:
                info = sys.exc_info()
                tbinfo = traceback.format_tb( info[2] )
                for tbi in tbinfo:
                    print tbi

    def setDataPy(self):
        if self.tab_widget_python !=  None:
            data = self.tab_widget_python.getConfData() 
            cdata = self.control_comp.convConfData(data)
            try:
                self.control_comp._rtcconf._ptr().setDataSeq_Py(cdata)
            except:
                info = sys.exc_info()
                tbinfo = traceback.format_tb( info[2] )
                for tbi in tbinfo:
                    print tbi
    
        
    def saveFile(self, filename):
        self.setDataCpp()
        self.setDataPy()
        
        try:
            wid = self.rtcd_widget.WidList["rtcList"]["Widget"]
            clist = []
            for c in range(0, wid.count()):
                clist.append(str(wid.itemText(c).toLocal8Bit()))
            self.control_comp._rtcconf._ptr().setExRTCList(clist)
            self.control_comp._rtcconf._ptr().save(filename)
        except:
            info = sys.exc_info()
            tbinfo = traceback.format_tb( info[2] )
            for tbi in tbinfo:
                print tbi

    def save(self):
        if self.curFile == "":
            return self.saveAs()
        else:
            self.saveFile(self.curFile)
            return True

    ##
    #ファイル保存のスロット
    ##
    def saveAs(self):
        
        fileName = QtGui.QFileDialog.getSaveFileName(self,u"保存", "","Config File (*.conf);;All Files (*)")
	if fileName.isEmpty():
            return False

	ba = str(fileName.toLocal8Bit())
	
        self.saveFile(ba)
        self.curFile = ba
        return True
	#self.tab_widget_python = None


        """fname = os.path.basename(ba)
        name, ext = os.path.splitext(fname)
        dname = os.path.dirname(os.path.relpath(ba))

        
        inv_dname = os.path.relpath(os.path.abspath(".\\"), dname)
        s = "cd " + inv_dname + "\n"
        s += "rtcd_python -f " + ".\\" + os.path.relpath(ba)

        if dname == "":
            path = ".\\"+name+".bat"
        else:
            path = dname+"\\"+name+".bat"
        pf = open(path, "w")
        pf.write(s)
        pf.close()


        
        for c in self.mgrc.mgr.getComponents():
            
            if dname == "":
                path = "./"+c.get_sdo_id() + ".conf"
            else:
                path = dname.replace("\\","/") + "/" +c.get_sdo_id() + ".conf"
            f2 = open(path, "w")

            s = c.getCategory() + "." + c.get_sdo_id() + ".config_file: " + path + "\n"
            f.write(s)

            
            cstes = c.get_configuration().get_active_configuration_set()
            s = "configuration.active_config: " + cstes.id + "\n"
            f2.write(s)
            
            for l in c.get_configuration().get_configuration_sets():
                for d in l.configuration_data:
                    s = "conf." + l.id + "." + d.name + ": " + d.value.value() + "\n"
                    f2.write(s)

            oEC = c.get_owned_contexts()[0]
            rate = oEC.get_rate()
            s = "exec_cxt.periodic.rate: " + str(rate) + "\n"
            f2.write(s)

            #s = "exec_cxt.periodic.type: " + "" + "\n"
            f2.close()
                
            



	f.close()"""

	

	

    ##
    #初期化のスロット
    ##
    def newFile(self):
        self.createTabs("rtc.conf")
        self.curFile = ""


        

    def mesBox(self, mes):
        msgbox = QtGui.QMessageBox( self )
        msgbox.setText( mes )
        msgbox.setModal( True )
        ret = msgbox.exec_()
