# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui',
# licensing of 'gui.ui' applies.
#
# Created: Thu Dec 26 10:37:54 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit_input = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_input.setObjectName("textEdit_input")
        self.gridLayout.addWidget(self.textEdit_input, 1, 0, 1, 1)
        self.textedit_output = QtWidgets.QTextEdit(self.centralwidget)
        self.textedit_output.setObjectName("textedit_output")
        self.gridLayout.addWidget(self.textedit_output, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.button_output = QtWidgets.QPushButton(self.centralwidget)
        self.button_output.setObjectName("button_output")
        self.gridLayout.addWidget(self.button_output, 2, 0, 1, 1)
        self.button_markdown_output = QtWidgets.QPushButton(self.centralwidget)
        self.button_markdown_output.setObjectName("button_markdown_output")
        self.gridLayout.addWidget(self.button_markdown_output, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Notes Point Extractor", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Input Text", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Output Text", None, -1))
        self.button_output.setText(QtWidgets.QApplication.translate("MainWindow", "Output", None, -1))
        self.button_markdown_output.setText(QtWidgets.QApplication.translate("MainWindow", "Markdown Output", None, -1))

