# !/usr/bin/python
# coding:utf-8

import sys
import base64
import tempfile
from PySide2 import QtCore, QtWidgets, QtGui
from fseutil.ui.main import Ui_MainWindow
from fseutil.ui.dialog_4_1_br187_parallel import Ui_dialog_4_1_br187_parallel
from fseutil.etc.images_base64 import dialog_4_1_br187_parallel_figure_1


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # pixmap = QtGui.QPixmap('/Users/ian/Desktop/phi calculator.png')
        # pixmap = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        # self.ui.label.setPixmap(pixmap)

        self.ui.b4_01_br187_parallel.clicked.connect(self.activate_b4_1)

    def activate_b4_1(self):
        b4_1 = Dialog0401_br187ParallelSimple(self)
        b4_1.show()
        b4_1.exec_()


class Dialog0401_br187ParallelSimple(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dialog0401_br187ParallelSimple, self).__init__(parent)
        self.ui = Ui_dialog_4_1_br187_parallel()
        self.ui.setupUi(self)

        _, fp_image_1 = tempfile.mkstemp()
        with open(fp_image_1, "wb") as f:
            f.write(base64.b64decode(dialog_4_1_br187_parallel_figure_1))

        pixmap = QtGui.QPixmap(fp_image_1)
        # pixmap = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        self.ui.label.setPixmap(pixmap)

        # self.ui.table.setRowCount(3)
        # self.ui.table.setColumnCount(4)
        #
        # self.ui.table.setHorizontalHeaderLabels(['aa', 'bb', 'cc', 'dd'])
        # for i in range(4):
        #     self.ui.table.setColumnWidth(i, 20)
        #
        # for i in range(3):
        #     for j in range(4):
        #         self.ui.table.setItem(i, j, QtWidgets.QTableWidgetItem(f'{i}{j}'))


def main():

    app = QtWidgets.QApplication(sys.argv)
    #
    window = MainWindow()
    window.show()

    # b4_1 = Dialog0401_br187ParallelSimple()
    # b4_1.show()
    #
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
