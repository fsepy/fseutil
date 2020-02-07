# !/usr/bin/python
# coding:utf-8

import sys

from PySide2 import QtCore, QtWidgets

from fseutil.guilogic.main import MainWindow

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


def main(app_window=None):
    app = QtWidgets.QApplication(sys.argv)
    if app_window is None:
        window = MainWindow()
    else:
        window = app_window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
