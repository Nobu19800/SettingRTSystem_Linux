# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ExComp import CompLayout


##
#並列ブロック追加ボタンを含むウィジェット
##
class AddButton3(QtGui.QWidget):
    clicked = QtCore.pyqtSignal(object, object)
    def __init__(self, text, parent=None):
        super(AddButton3, self).__init__(parent)
        
        self.Vl = None
        self.c = None
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
        
        self.clicked.emit(self.Vl, self.c)
