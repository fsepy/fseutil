# !/usr/bin/python
# coding:utf-8

import sys
import base64
import tempfile
from PySide2 import QtCore, QtWidgets, QtGui
from fseutil.ui.main import Ui_MainWindow
from fseutil.ui.dialog_4_1_br187_parallel_simple import Ui_dialog_4_1_br187_parallel_simple
from fseutil.ui.dialog_1_1_adb_datasheet_1 import Ui_dialog_1_1_adb_datasheet_1
from fseutil.etc.images_base64 import OFR_LOGO_LARGE_PNG_BASE64
from fseutil.etc.images_base64 import dialog_4_1_br187_parallel_figure_1
from fseutil.etc.images_base64 import dialog_1_1_adb2_datasheet_1

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        _, fp_image_1 = tempfile.mkstemp()
        with open(fp_image_1, "wb") as f:
            f.write(base64.b64decode(OFR_LOGO_LARGE_PNG_BASE64))

        pixmap = QtGui.QPixmap(fp_image_1)
        self.ui.label_logo.setPixmap(pixmap)

        self.ui.b4_01_br187_parallel.clicked.connect(self.activate_0401_br187_parallel_simple)
        self.ui.btn_b1_01_adb2_datasheet_1.clicked.connect(self.activate_0101_adb2_datasheet_1)

    def activate_0401_br187_parallel_simple(self):
        b4_1 = Dialog0401_br187ParallelSimple(self)
        b4_1.show()
        b4_1.exec_()

    def activate_0101_adb2_datasheet_1(self):
        b4_1 = Dialog0101_ADB2Datasheet1(self)
        b4_1.show()
        b4_1.exec_()


class Dialog0401_br187ParallelSimple(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dialog0401_br187ParallelSimple, self).__init__(parent)
        self.ui = Ui_dialog_4_1_br187_parallel_simple()
        self.ui.setupUi(self)

        _, fp_image_1 = tempfile.mkstemp()
        with open(fp_image_1, "wb") as f:
            f.write(base64.b64decode(dialog_4_1_br187_parallel_figure_1))

        pixmap = QtGui.QPixmap(fp_image_1)
        self.ui.label.setPixmap(pixmap)

        # self.ui.table.setRowCount(3)
        # self.ui.table.setColumnCount(4)
        # self.ui.table.setHorizontalHeaderLabels(['aa', 'bb', 'cc', 'dd'])
        # for i in range(4):
        #     self.ui.table.setColumnWidth(i, 20)
        # for i in range(3):
        #     for j in range(4):
        #         self.ui.table.setItem(i, j, QtWidgets.QTableWidgetItem(f'{i}{j}'))


class Dialog0101_ADB2Datasheet1(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dialog0101_ADB2Datasheet1, self).__init__(parent)
        self.ui = Ui_dialog_1_1_adb_datasheet_1()
        self.ui.setupUi(self)

        _, fp_image_1 = tempfile.mkstemp()
        with open(fp_image_1, "wb") as f:
            f.write(base64.b64decode(dialog_1_1_adb2_datasheet_1))

        pixmap = QtGui.QPixmap(fp_image_1)
        self.ui.label.setPixmap(pixmap)


def main(AppWindow=None):

    app = QtWidgets.QApplication(sys.argv)
    if AppWindow is None:
        window = MainWindow()
    else:
        window = AppWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
