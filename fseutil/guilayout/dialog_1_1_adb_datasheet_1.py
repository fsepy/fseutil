# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\IanFu\Documents\github\fseutil\fseutil\guilayout\ui\dialog_1_1_adb_datasheet_1.ui',
# licensing of 'C:\Users\IanFu\Documents\github\fseutil\fseutil\guilayout\ui\dialog_1_1_adb_datasheet_1.ui' applies.
#
# Created: Tue Feb  4 13:42:35 2020
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_dialog_1_1_adb_datasheet_1(object):
    def setupUi(self, dialog_1_1_adb_datasheet_1):
        dialog_1_1_adb_datasheet_1.setObjectName("dialog_1_1_adb_datasheet_1")
        dialog_1_1_adb_datasheet_1.resize(833, 625)
        self.scrollArea = QtWidgets.QScrollArea(dialog_1_1_adb_datasheet_1)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 800, 600))
        self.scrollArea.setMaximumSize(QtCore.QSize(800, 600))
        self.scrollArea.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 781, 581))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setGeometry(QtCore.QRect(10, 10, 947, 670))
        self.label.setMinimumSize(QtCore.QSize(947, 670))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images/adb2_datasheet_1_947_670.png"))
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(dialog_1_1_adb_datasheet_1)
        QtCore.QMetaObject.connectSlotsByName(dialog_1_1_adb_datasheet_1)

    def retranslateUi(self, dialog_1_1_adb_datasheet_1):
        dialog_1_1_adb_datasheet_1.setWindowTitle(QtWidgets.QApplication.translate("dialog_1_1_adb_datasheet_1", "ADB Vol. 2 2019 Data Sheet No. 1", None, -1))

