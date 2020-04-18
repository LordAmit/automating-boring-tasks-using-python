# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.button_pdf_save = QtWidgets.QPushButton(self.centralwidget)
        self.button_pdf_save.setObjectName("button_pdf_save")
        self.gridLayout_2.addWidget(self.button_pdf_save, 3, 2, 1, 1)
        self.button_delete = QtWidgets.QPushButton(self.centralwidget)
        self.button_delete.setObjectName("button_delete")
        self.gridLayout_2.addWidget(self.button_delete, 1, 1, 1, 1)
        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.gridLayout_2.addWidget(self.slider, 1, 2, 1, 1)
        self.button_reset = QtWidgets.QPushButton(self.centralwidget)
        self.button_reset.setObjectName("button_reset")
        self.gridLayout_2.addWidget(self.button_reset, 1, 0, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 0, 0, 1, 3)
        self.button_browse_pdf = QtWidgets.QPushButton(self.centralwidget)
        self.button_browse_pdf.setObjectName("button_browse_pdf")
        self.gridLayout_2.addWidget(self.button_browse_pdf, 3, 0, 1, 2)
        self.button_save = QtWidgets.QPushButton(self.centralwidget)
        self.button_save.setObjectName("button_save")
        self.gridLayout_2.addWidget(self.button_save, 2, 2, 1, 1)
        self.button_browse = QtWidgets.QPushButton(self.centralwidget)
        self.button_browse.setObjectName("button_browse")
        self.gridLayout_2.addWidget(self.button_browse, 2, 0, 1, 2)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Scanned Image Beautifier"))
        self.button_pdf_save.setText(_translate("MainWindow", "Save as PDF"))
        self.button_delete.setText(_translate("MainWindow", "Delete"))
        self.button_reset.setText(_translate("MainWindow", "Reset"))
        self.button_browse_pdf.setText(_translate("MainWindow", "Browse PDF"))
        self.button_save.setText(_translate("MainWindow", "Save"))
        self.button_browse.setText(_translate("MainWindow", "Browse"))
