# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from FEComp import FEComp

##
#ブロック追加ボタンを含むウィジェット
##
class AddButton(QtGui.QWidget):
    clicked = QtCore.pyqtSignal(object)
    def __init__(self, text, parent=None):
        super(AddButton, self).__init__(parent)
        
        self.Fc = None
        self.PB = QtGui.QPushButton(text)
        self.mainLayout = QtGui.QVBoxLayout()
        
        #connect(PB, SIGNAL(clicked()),
        #    this, SLOT(clickedSlot()))
        #QtCore.QObject.connect(self.PB, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("clickedSlot()"))

        self.PB.clicked.connect(self.clickedSlot)

        self.mainLayout.addWidget(self.PB)

        self.setLayout(self.mainLayout)

        
        
    ##
    #ボタンクリック時に呼び出すスロット
    ##
    def clickedSlot(self):
        print self.Fc
        self.clicked.emit(self.Fc)
