# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ian\Documents\GitHub\fseutil\gui\main.ui',
# licensing of 'C:\Users\ian\Documents\GitHub\fseutil\gui\main.ui' applies.
#
# Created: Wed Jan 22 23:12:36 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 520)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 130, 501, 101))
        self.groupBox.setObjectName("groupBox")
        self.b4_01_br187_parallel = QtWidgets.QPushButton(self.groupBox)
        self.b4_01_br187_parallel.setGeometry(QtCore.QRect(20, 20, 70, 70))
        self.b4_01_br187_parallel.setObjectName("b4_01_br187_parallel")
        self.b4_02_perpendicular = QtWidgets.QPushButton(self.groupBox)
        self.b4_02_perpendicular.setGeometry(QtCore.QRect(90, 20, 70, 70))
        self.b4_02_perpendicular.setObjectName("b4_02_perpendicular")
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(310, 30, 194, 80))
        self.label_logo.setText("")
        self.label_logo.setPixmap(QtGui.QPixmap("ofr-colour-194_80.png"))
        self.label_logo.setObjectName("label_logo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionhello_1 = QtWidgets.QAction(MainWindow)
        self.actionhello_1.setObjectName("actionhello_1")
        self.actionhello_2 = QtWidgets.QAction(MainWindow)
        self.actionhello_2.setObjectName("actionhello_2")
        self.actionhello_3 = QtWidgets.QAction(MainWindow)
        self.actionhello_3.setObjectName("actionhello_3")
        self.actionhello = QtWidgets.QAction(MainWindow)
        self.actionhello.setObjectName("actionhello")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "B4 External flame spread", None, -1))
        self.b4_01_br187_parallel.setText(QtWidgets.QApplication.translate("MainWindow", "BR 187\n"
"Parallel", None, -1))
        self.b4_02_perpendicular.setText(QtWidgets.QApplication.translate("MainWindow", "BR 187\n"
"Perp.", None, -1))
        self.actionhello_1.setText(QtWidgets.QApplication.translate("MainWindow", "hello 1", None, -1))
        self.actionhello_2.setText(QtWidgets.QApplication.translate("MainWindow", "hello 2", None, -1))
        self.actionhello_3.setText(QtWidgets.QApplication.translate("MainWindow", "hello 3", None, -1))
        self.actionhello.setText(QtWidgets.QApplication.translate("MainWindow", "hello", None, -1))

