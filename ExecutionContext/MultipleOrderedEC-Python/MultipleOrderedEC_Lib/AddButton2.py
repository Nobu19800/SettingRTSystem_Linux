# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ExComp import CompLayout


##
#直列ブロック追加ボタンを含むウィジェット
##
class AddButton2(QtGui.QWidget):
    clicked = QtCore.pyqtSignal(object)
    def __init__(self, text, parent=None):
        super(AddButton2, self).__init__(parent)
        
        self.Cl = None
        self.PB = QtGui.QPushButton(text)
        self.mainLayout = QtGui.QVBoxLayout()
        
        #connect(PB, SIGNAL(clicked()),
        #    this, SLOT(clickedSlot()))

        self.PB.clicked.connect(self.clickedSlot)

        self.mainLayout.addWidget(self.PB)

        self.setLayout(self.mainLayout)

    ##
    #ボタンクリック時に呼び出すスロット
    ##
    def clickedSlot(self):
        
        self.clicked.emit(self.Cl)
