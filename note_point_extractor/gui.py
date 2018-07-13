# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit_input = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_input.setObjectName(_fromUtf8("textEdit_input"))
        self.gridLayout.addWidget(self.textEdit_input, 1, 0, 1, 1)
        self.textedit_output = QtGui.QTextEdit(self.centralwidget)
        self.textedit_output.setObjectName(_fromUtf8("textedit_output"))
        self.gridLayout.addWidget(self.textedit_output, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.button_output = QtGui.QPushButton(self.centralwidget)
        self.button_output.setObjectName(_fromUtf8("button_output"))
        self.gridLayout.addWidget(self.button_output, 2, 0, 1, 1)
        self.button_markdown_output = QtGui.QPushButton(self.centralwidget)
        self.button_markdown_output.setObjectName(_fromUtf8("button_markdown_output"))
        self.gridLayout.addWidget(self.button_markdown_output, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Notes Point Extractor", None))
        self.label.setText(_translate("MainWindow", "Input Text", None))
        self.label_2.setText(_translate("MainWindow", "Output Text", None))
        self.button_output.setText(_translate("MainWindow", "Output", None))
        self.button_markdown_output.setText(_translate("MainWindow", "Markdown Output", None))

