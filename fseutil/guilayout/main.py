# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\IanFu\Documents\github\fseutil\fseutil\guilayout\ui\main.ui',
# licensing of 'C:\Users\IanFu\Documents\github\fseutil\fseutil\guilayout\ui\main.ui' applies.
#
# Created: Tue Feb  4 13:42:34 2020
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(474, 614)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(260, 5, 194, 80))
        self.label_logo.setText("")
        self.label_logo.setPixmap(QtGui.QPixmap("guilayout/images/ofr-colour-194_80.png"))
        self.label_logo.setObjectName("label_logo")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 20, 231, 71))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(10, 30, 211, 16))
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 0, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 86, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 350, 181, 101))
        self.groupBox_4.setObjectName("groupBox_4")
        self.b4_01_br187_parallel_7 = QtWidgets.QPushButton(self.groupBox_4)
        self.b4_01_br187_parallel_7.setGeometry(QtCore.QRect(10, 20, 70, 70))
        self.b4_01_br187_parallel_7.setObjectName("b4_01_br187_parallel_7")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 230, 371, 101))
        self.groupBox_3.setObjectName("groupBox_3")
        self.b4_01_br187_parallel_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.b4_01_br187_parallel_2.setGeometry(QtCore.QRect(80, 20, 70, 70))
        self.b4_01_br187_parallel_2.setObjectName("b4_01_br187_parallel_2")
        self.b4_01_br187_parallel_8 = QtWidgets.QPushButton(self.groupBox_3)
        self.b4_01_br187_parallel_8.setGeometry(QtCore.QRect(150, 20, 70, 70))
        self.b4_01_br187_parallel_8.setObjectName("b4_01_br187_parallel_8")
        self.pushButton_0111_heat_detector_activation = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_0111_heat_detector_activation.setGeometry(QtCore.QRect(220, 20, 70, 70))
        self.pushButton_0111_heat_detector_activation.setObjectName("pushButton_0111_heat_detector_activation")
        self.b4_01_br187_parallel_10 = QtWidgets.QPushButton(self.groupBox_3)
        self.b4_01_br187_parallel_10.setGeometry(QtCore.QRect(290, 20, 70, 70))
        self.b4_01_br187_parallel_10.setObjectName("b4_01_br187_parallel_10")
        self.pushButton_0101_adb2_datasheet_1 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_0101_adb2_datasheet_1.setGeometry(QtCore.QRect(10, 20, 70, 70))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_0101_adb2_datasheet_1.setFont(font)
        self.pushButton_0101_adb2_datasheet_1.setCursor(QtCore.Qt.ArrowCursor)
        self.pushButton_0101_adb2_datasheet_1.setObjectName("pushButton_0101_adb2_datasheet_1")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 120, 91, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_0601_naming_convention = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_0601_naming_convention.setGeometry(QtCore.QRect(10, 20, 70, 70))
        self.pushButton_0601_naming_convention.setObjectName("pushButton_0601_naming_convention")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 460, 301, 101))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_0401_br187_parallel_simple = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_0401_br187_parallel_simple.setGeometry(QtCore.QRect(10, 20, 70, 70))
        self.pushButton_0401_br187_parallel_simple.setObjectName("pushButton_0401_br187_parallel_simple")
        self.pushButton_0402_br187_perpendicular_simple = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_0402_br187_perpendicular_simple.setGeometry(QtCore.QRect(80, 20, 70, 70))
        self.pushButton_0402_br187_perpendicular_simple.setObjectName("pushButton_0402_br187_perpendicular_simple")
        self.pushButton_0403_br187_parallel_complex = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_0403_br187_parallel_complex.setGeometry(QtCore.QRect(150, 20, 70, 70))
        self.pushButton_0403_br187_parallel_complex.setObjectName("pushButton_0403_br187_parallel_complex")
        self.pushButton_0404_br187_perpendicular_complex = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_0404_br187_perpendicular_complex.setGeometry(QtCore.QRect(220, 20, 70, 70))
        self.pushButton_0404_br187_perpendicular_complex.setObjectName("pushButton_0404_br187_perpendicular_complex")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 474, 21))
        self.menubar.setObjectName("menubar")
        self.menuHello_world = QtWidgets.QMenu(self.menubar)
        self.menuHello_world.setObjectName("menuHello_world")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHello_world.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "© OFR Consultants Ltd. All rights reserved.", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "OFR FSEUTL", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Version 0.0.1", None, -1))
        self.groupBox_4.setTitle(QtWidgets.QApplication.translate("MainWindow", "B3 Internal fire spread (structure)", None, -1))
        self.b4_01_br187_parallel_7.setText(QtWidgets.QApplication.translate("MainWindow", "Compatment\n"
"Size", None, -1))
        self.groupBox_3.setTitle(QtWidgets.QApplication.translate("MainWindow", "B1 Means of escape", None, -1))
        self.b4_01_br187_parallel_2.setText(QtWidgets.QApplication.translate("MainWindow", "BS 9999\n"
"Datasheet\n"
"No. 1", None, -1))
        self.b4_01_br187_parallel_8.setText(QtWidgets.QApplication.translate("MainWindow", "Merging\n"
"Flow", None, -1))
        self.pushButton_0111_heat_detector_activation.setText(QtWidgets.QApplication.translate("MainWindow", "HD\n"
"Activation\n"
"Time", None, -1))
        self.b4_01_br187_parallel_10.setText(QtWidgets.QApplication.translate("MainWindow", "Zone\n"
"Model", None, -1))
        self.pushButton_0101_adb2_datasheet_1.setText(QtWidgets.QApplication.translate("MainWindow", "ADB 2\n"
"Datasheet\n"
"No. 1", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("MainWindow", "Miscellaneous", None, -1))
        self.pushButton_0601_naming_convention.setText(QtWidgets.QApplication.translate("MainWindow", "File\n"
"Naming\n"
"Protocol", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "B4 External flame spread", None, -1))
        self.pushButton_0401_br187_parallel_simple.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Thermal radiation calculation methodology in accordance with BR 187, only for parallel faced emitter receiver arrangement.", None, -1))
        self.pushButton_0401_br187_parallel_simple.setText(QtWidgets.QApplication.translate("MainWindow", "BR 187\n"
"Parallel", None, -1))
        self.pushButton_0402_br187_perpendicular_simple.setText(QtWidgets.QApplication.translate("MainWindow", "BR 187\n"
"Perp.", None, -1))
        self.pushButton_0403_br187_parallel_complex.setText(QtWidgets.QApplication.translate("MainWindow", "BR 187\n"
"Parallel\n"
"Complex", None, -1))
        self.pushButton_0404_br187_perpendicular_complex.setText(QtWidgets.QApplication.translate("MainWindow", "BR 187\n"
"Perp.\n"
"Complex", None, -1))
        self.menuHello_world.setTitle(QtWidgets.QApplication.translate("MainWindow", "Hello world", None, -1))

