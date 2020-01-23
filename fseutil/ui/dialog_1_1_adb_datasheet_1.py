# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\IanFu\Documents\github\fseutil\gui\dialog_1_1_adb_datasheet_1.ui',
# licensing of 'C:\Users\IanFu\Documents\github\fseutil\gui\dialog_1_1_adb_datasheet_1.ui' applies.
#
# Created: Thu Jan 23 18:34:05 2020
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(970, 690)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 947, 670))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images/adb2_datasheet_1_947_670.png"))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))

