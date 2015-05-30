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

from SettingRTCConf.MTabWidget import MTabWidget


##
# @class TreeNode
# @brief ツリーノード
#
class TreeNode:
    ##
    # @brief コンストラクタ
    # @param self 
    # @param node ツリーアイテム
    # @param mw メインウインドウオブジェクト
    def __init__(self, node, mw):
        self.node = node
        self.window = mw
    ##
    # @brief 子ノード追加
    # @param self
    # @param child 子ノード
    def appendChild(self, child):
        self.node.addChild(child.node)
    ##
    # @brief 親ノード取得
    # @param self
    # @return 親ノード
    def getParent(self):
        parent = self.node.parent()
        if parent == None:
            return None
        return self.window.getTreeNode(parent)
    ##
    # @brief 子ノード数取得
    # @param self
    # @return 子ノード数
    def getChildCount(self):
        return int(self.node.childCount())
    ##
    # @brief 表示名取得
    # @param self
    # @return 表示名
    def getDisplayValue(self):
        return str(self.node.text(0).toLocal8Bit())


class rtcdWidget(MTabWidget):
    
    def __init__(self, parent=None):
        MTabWidget.__init__(self, None, parent)
        self.parent = parent
        self.addTextBox("textBox", u"IPアドレス", ["localhost"] , "localhost")
        self.addTextBox("filepath", u"ファイル名", [""] , "")

        self.addFilePathButton = QtGui.QPushButton(u"ファイル名設定")
        self.WidList["filepath"]["Layout"].addWidget(self.addFilePathButton)
        self.addFilePathButton.clicked.connect(self.addFilePathSlot)

        self.addLoadButton = QtGui.QPushButton(u"ファイル読み込み")
        self.WidList["filepath"]["Layout"].addWidget(self.addLoadButton)
        self.addLoadButton.clicked.connect(self.addLoadSlot)


        self.newFileButton = QtGui.QPushButton(u"新規作成")
        self.WidList["filepath"]["Layout"].addWidget(self.newFileButton)
        self.newFileButton.clicked.connect(self.newFileSlot)


        self.saveFileButton = QtGui.QPushButton(u"ファイル保存")
        self.WidList["filepath"]["Layout"].addWidget(self.saveFileButton)
        self.saveFileButton.clicked.connect(self.saveFileSlot)

        self.rtcdButton = QtGui.QPushButton(u"rtcd起動")
        self.WidList["filepath"]["Layout"].addWidget(self.rtcdButton)
        self.rtcdButton.clicked.connect(self.rtcdSlot)

        
        self.treelayout = QtGui.QVBoxLayout()
        
        self.treeWidget = QtGui.QTreeWidget(self)
        self.treelayout.addWidget(self.treeWidget)
        self.treeWidget.itemClicked.connect(self.treeWidgetSlot)

        self.updateTreeButton = QtGui.QPushButton(u"RTCツリー更新")
        self.treelayout.addWidget(self.updateTreeButton)
        self.updateTreeButton.clicked.connect(self.updateTreeSlot)

        self.addCombox("rtcList", u"システムに加える外部のRTC一覧", [], [] , "")

        self.addRTCButton = QtGui.QPushButton(u"外部のRTCをシステムに追加")
        self.treelayout.addWidget(self.addRTCButton)
        self.addRTCButton.clicked.connect(self.addRTCSlot)

        self.remRTCButton = QtGui.QPushButton(u"外部のRTCをシステムから削除")
        self.treelayout.addWidget(self.remRTCButton)
        self.remRTCButton.clicked.connect(self.remRTCSlot)

        

        self.treeNodeList = []
        self.mainLayout.addLayout(self.treelayout)

        self.compList = []

        self.selItem = None
        #print self.getRTCList("localhost")
        #self.setRTCTree()
        #print self.compList

    def addRTCSlot(self):
        
        rtc = self.getSelectRTC()
        if rtc:
            s = ""
            for i in range(0,len(rtc)):
                s += rtc[i]
                if i != 0 and i != len(rtc)-1:
                    s += "/"
            wid = self.WidList["rtcList"]["Widget"]
            if wid.findText(s) == -1:        
                wid.addItem(s)

    def remRTCSlot(self):
        wid = self.WidList["rtcList"]["Widget"]
        wid.removeItem(wid.findText(wid.currentText()))

    ##
    # @brief ツリーのマウスでの操作に対するコールバック
    # @param self 
    #
    def treeWidgetSlot(self, obj):
        
        self.selItem = self.getTreeNode(obj)
        #print self.getSelectRTC()

    def getSelectRTC(self):
        mlist = []
        node = self.selItem


        if node:
            
            parent = node.getParent()
            
            if parent:
                mlist.insert(0, node.getDisplayValue())
            else:
                return None
            if node.getChildCount() != 0:
                return None
        else:
            return None
        while(True):
            if node:
                node = node.getParent()
                if node:
                    mlist.insert(0, node.getDisplayValue())
                else:
                    break
        for c in self.compList:
            if mlist == c:
                return c
        
        return None
    ##
    # @brief 選択中のツリーアイテム取得
    # @param self 
    # @return 選択中のツリーアイテム
    #
    def getSelection(self):
        return self.selItem
    
    def updateTreeSlot(self):
        self.setRTCTree()

    def setRTCTree(self):
        self.treeWidget.clear()
        self.treeNodeList = []

        tmp = QtGui.QTreeWidgetItem(["/"])
        self.treeWidget.addTopLevelItem(tmp)
        root = TreeNode(tmp, self)
        self.treeNodeList.append(root)

        ipaddress = str(self.WidList["textBox"]["Widget"].text().toLocal8Bit())

        self.compList = self.getRTCList(ipaddress, root)
        
            

        

    def getTreeNode(self, obj):
        for i in self.treeNodeList:
            if i.node == obj:
                return i
        return None
    
    def createNode(self, name, sel):
        tmp = TreeNode(QtGui.QTreeWidgetItem([name]), self)
        self.treeNodeList.append(tmp)
        return tmp
    
    def getRTCList(self, server, oParent):
         self.tree = rtctree.tree.RTCTree(servers=server,orb=self.parent.control_comp._manager.getORB())
         plist = []
         path = ["/"]
         self.getNode(self.tree._root, path, plist, oParent)
         return plist
        
    def getNode(self, node, path, plist, oParent):
        
        values = node._children.values()
        
        for v in values:
            
            
            if v.is_component:
                oChild = self.createNode(v.name,False)
                oParent.appendChild(oChild)
                
                tmpPath = path[:]
                tmpPath.append(v.name)
                plist.append(tmpPath[:])
            elif v.is_manager:
                pass
            elif v.is_directory or v.is_nameserver:
                oChild = self.createNode(v.name,False)
                oParent.appendChild(oChild)
                
                tmpPath = path[:]
                tmpPath.append(v.name)
                self.getNode(v,tmpPath,plist,oChild)
            
                

    def rtcdSlot(self):
        try:
            self.parent.setDataCpp()
            self.parent.setDataPy()
            self.parent.control_comp._rtcconf._ptr().startRTCD_Cpp()
            self.parent.control_comp._rtcconf._ptr().startRTCD_Py()

            

            self.parent.control_comp._rtcconf._ptr().setSystem()
        except:
            info = sys.exc_info()
            tbinfo = traceback.format_tb( info[2] )
            for tbi in tbinfo:
                print tbi

    def addLoadSlot(self):
        path = str(self.WidList["filepath"]["Widget"].text().toLocal8Bit())
        if path != "":
            self.parent.createTabs(path)
            self.parent.curFile = path
        else:
            self.mesBox(u"ファイル名を入力してください")

    def addFilePathSlot(self):
        wid = self.WidList["filepath"]["Widget"]
        text = self.parent.getFilePath()
        self.WidList["filepath"]["Widget"].setText(text)
            
        
        wid.setText(text)

    def newFileSlot(self):
        self.parent.newFile()
        
    def saveFileSlot(self):
        path = str(self.WidList["filepath"]["Widget"].text().toLocal8Bit())
        if path != "":
            self.parent.saveFile(path)
            self.parent.curFile = path
        else:
            self.mesBox(u"ファイル名を入力してください")

    def delLangSlot(self):
        wid = self.WidList["manager.supported_languages"]["Widget"]
        wid.removeItem(wid.findText(wid.currentText()))

    def createCompSlot(self):
        wid = self.WidList["manager.components.precreate"]["Widget"]
        s = str(wid.currentText().toLocal8Bit())
        
        comp = self.mgrc.mgr.createComponent(s)
        if not comp:
            self.mesBox(u"RTCの起動に失敗しました")
            return
        wid.addItem(wid.currentText())

        self.mgrc.addComp(s, comp)

    def delCompSlot(self):
        wid = self.WidList["manager.components.precreate"]["Widget"]
        self.mgrc.deleteComp(str(wid.currentText().toLocal8Bit()))
        wid.removeItem(wid.findText(wid.currentText()))

        

    def delModuleSlot(self):
        wid = self.WidList["manager.modules.preload"]["Widget"]
        wid.removeItem(wid.findText(wid.currentText()))

    def delPathSlot(self):
        wid = self.WidList["manager.modules.load_path"]["Widget"]
        wid.removeItem(wid.findText(wid.currentText()))

    def loadRTCSlot(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","","Python File (*.py);;All Files (*)")

        if fileName.isEmpty():
            return
        ba = str(fileName.toLocal8Bit())
        fname = os.path.basename(ba)
        name, ext = os.path.splitext(fname)
        dname = os.path.dirname(os.path.relpath(ba))
        if self.mgrc.createComp(name,[dname]) == False:
            self.mesBox(u"モジュールの読み込みに失敗しました")
            return

        wid = self.WidList["manager.components.precreate"]["Widget"]
        wid.addItem(name)

        wid = self.WidList["manager.modules.preload"]["Widget"]
        if wid.findText(fname) == -1:
            wid.addItem(fname)

        wid = self.WidList["manager.modules.load_path"]["Widget"]

        if dname == "":
            dname = "./" + dname
        if wid.findText(dname) == -1:
            
            wid.addItem(dname)
