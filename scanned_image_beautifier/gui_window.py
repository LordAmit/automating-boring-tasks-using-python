# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_window.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.button_delete = QtGui.QPushButton(self.centralwidget)
        self.button_delete.setObjectName(_fromUtf8("button_delete"))
        self.gridLayout_2.addWidget(self.button_delete, 1, 1, 1, 1)
        self.slider = QtGui.QSlider(self.centralwidget)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName(_fromUtf8("slider"))
        self.gridLayout_2.addWidget(self.slider, 1, 2, 1, 1)
        self.button_reset = QtGui.QPushButton(self.centralwidget)
        self.button_reset.setObjectName(_fromUtf8("button_reset"))
        self.gridLayout_2.addWidget(self.button_reset, 1, 0, 1, 1)
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout_2.addWidget(self.graphicsView, 0, 0, 1, 3)
        self.button_browse = QtGui.QPushButton(self.centralwidget)
        self.button_browse.setObjectName(_fromUtf8("button_browse"))
        self.gridLayout_2.addWidget(self.button_browse, 3, 0, 1, 1)
        self.button_save = QtGui.QPushButton(self.centralwidget)
        self.button_save.setObjectName(_fromUtf8("button_save"))
        self.gridLayout_2.addWidget(self.button_save, 3, 2, 1, 1)
        self.button_grayscale = QtGui.QPushButton(self.centralwidget)
        self.button_grayscale.setObjectName(_fromUtf8("button_grayscale"))
        self.gridLayout_2.addWidget(self.button_grayscale, 3, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Scanned Image Beautifier", None))
        self.button_delete.setText(_translate("MainWindow", "Delete", None))
        self.button_reset.setText(_translate("MainWindow", "Reset", None))
        self.button_browse.setText(_translate("MainWindow", "Browse", None))
        self.button_save.setText(_translate("MainWindow", "Save", None))
        self.button_grayscale.setText(_translate("MainWindow", "Grayscale", None))

