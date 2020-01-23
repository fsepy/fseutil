# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\IanFu\Documents\github\fseutil\gui\main.ui',
# licensing of 'C:\Users\IanFu\Documents\github\fseutil\gui\main.ui' applies.
#
# Created: Thu Jan 23 18:34:05 2020
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 639)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 470, 301, 101))
        self.groupBox.setObjectName("groupBox")
        self.b4_01_br187_parallel = QtWidgets.QPushButton(self.groupBox)
        self.b4_01_br187_parallel.setGeometry(QtCore.QRect(10, 20, 70, 70))
        self.b4_01_br187_parallel.setObjectName("b4_01_br187_parallel")
        self.b4_02_perpendicular = QtWidgets.QPushButton(self.groupBox)
        self.b4_02_perpendicular.setGeometry(QtCore.QRect(80, 20, 70, 70))
        self.b4_02_perpendicular.setObjectName("b4_02_perpendicular")
        self.b4_01_br187_parallel_4 = QtWidgets.QPushButton(self.groupBox)
        self.b4_01_br187_parallel_4.setGeometry(QtCore.QRect(150, 20, 70, 70))
        self.b4_01_br187_parallel_4.setObjectName("b4_01_br187_parallel_4")
        self.b4_01_br187_parallel_5 = QtWidgets.QPushButton(self.groupBox)
        self.b4_01_br187_parallel_5.setGeometry(QtCore.QRect(220, 20, 70, 70))
        self.b4_01_br187_parallel_5.setObjectName("b4_01_br187_parallel_5")
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(310, 30, 194, 80))
        self.label_logo.setText("")
        self.label_logo.setPixmap(QtGui.QPixmap("images/ofr-colour-194_80.png"))
        self.label_logo.setObjectName("label_logo")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 130, 91, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.b4_01_br187_parallel_6 = QtWidgets.QPushButton(self.groupBox_2)
        self.b4_01_br187_parallel_6.setGeometry(QtCore.QRect(10, 20, 70, 70))
        self.b4_01_br187_parallel_6.setObjectName("b4_01_br187_parallel_6")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 240, 371, 101))
        self.groupBox_3.setObjectName("groupBox_3")
        self.b4_01_br187_parallel_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.b4_01_br187_parallel_2.setGeometry(QtCore.QRect(10, 20, 70, 70))
        self.b4_01_br187_parallel_2.setObjectName("b4_01_br187_parallel_2")
        self.b4_01_br187_parallel_3 = QtWidgets.QPushButton(self.groupBox_3)
        self.b4_01_br187_parallel_3.setGeometry(QtCore.QRect(80, 20, 70, 70))
        self.b4_01_br187_parallel_3.setObjectName("b4_01_br187_parallel_3")
        self.b4_01_br187_parallel_8 = QtWidgets.QPushButton(self.groupBox_3)
        self.b4_01_br187_parallel_8.setGeometry(QtCore.QRect(150, 20, 70, 70))
        self.b4_01_br187_parallel_8.setObjectName("b4_01_br187_parallel_8")
        self.b4_01_br187_parallel_9 = QtWidgets.QPushButton(self.groupBox_3)
        self.b4_01_br187_parallel_9.setGeometry(QtCore.QRect(220, 20, 70, 70))
        self.b4_01_br187_parallel_9.setObjectName("b4_01_br187_parallel_9")
        self.b4_01_br187_parallel_10 = QtWidgets.QPushButton(self.groupBox_3)
        self.b4_01_br187_parallel_10.setGeometry(QtCore.QRect(290, 20, 70, 70))
        self.b4_01_br187_parallel_10.setObjectName("b4_01_br187_parallel_10")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 360, 181, 101))
        self.groupBox_4.setObjectName("groupBox_4")
        self.b4_01_br187_parallel_7 = QtWidgets.QPushButton(self.groupBox_4)
        self.b4_01_br187_parallel_7.setGeometry(QtCore.QRect(10, 20, 70, 70))
        self.b4_01_br187_parallel_7.setObjectName("b4_01_br187_parallel_7")
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
        self.b4_01_br187_parallel_4.setText(QtWidgets.QApplication.translate("MainWindow", "BR 187\n"
"Parallel\n"
"Complex", None, -1))
        self.b4_01_br187_parallel_5.setText(QtWidgets.QApplication.translate("MainWindow", "BR 187\n"
"Perp.\n"
"Complex", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("MainWindow", "Miscellaneous", None, -1))
        self.b4_01_br187_parallel_6.setText(QtWidgets.QApplication.translate("MainWindow", "File\n"
"Naming\n"
"Protocol", None, -1))
        self.groupBox_3.setTitle(QtWidgets.QApplication.translate("MainWindow", "B1 Means of escape", None, -1))
        self.b4_01_br187_parallel_2.setText(QtWidgets.QApplication.translate("MainWindow", "BS 9999\n"
"Datasheet\n"
"No. 1", None, -1))
        self.b4_01_br187_parallel_3.setText(QtWidgets.QApplication.translate("MainWindow", "ADB 2\n"
"Datasheet\n"
"No. 1", None, -1))
        self.b4_01_br187_parallel_8.setText(QtWidgets.QApplication.translate("MainWindow", "Merging\n"
"Flow", None, -1))
        self.b4_01_br187_parallel_9.setText(QtWidgets.QApplication.translate("MainWindow", "HD\n"
"Activation\n"
"Time", None, -1))
        self.b4_01_br187_parallel_10.setText(QtWidgets.QApplication.translate("MainWindow", "Zone\n"
"Model", None, -1))
        self.groupBox_4.setTitle(QtWidgets.QApplication.translate("MainWindow", "B3 Internal fire spread (structure)", None, -1))
        self.b4_01_br187_parallel_7.setText(QtWidgets.QApplication.translate("MainWindow", "Compatment\n"
"Size", None, -1))
        self.actionhello_1.setText(QtWidgets.QApplication.translate("MainWindow", "hello 1", None, -1))
        self.actionhello_2.setText(QtWidgets.QApplication.translate("MainWindow", "hello 2", None, -1))
        self.actionhello_3.setText(QtWidgets.QApplication.translate("MainWindow", "hello 3", None, -1))
        self.actionhello.setText(QtWidgets.QApplication.translate("MainWindow", "hello", None, -1))

