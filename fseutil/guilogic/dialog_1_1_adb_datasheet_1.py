from PySide2 import QtWidgets, QtGui, QtCore

from fseutil.etc.images_base64 import dialog_1_1_adb2_datasheet_1
from fseutil.guilayout.dialog_1_1_adb_datasheet_1 import Ui_Dialog


class Dialog0101_ADB2Datasheet1(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dialog0101_ADB2Datasheet1, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        ba = QtCore.QByteArray.fromBase64(dialog_1_1_adb2_datasheet_1)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.ui.label.setPixmap(pix_map)

        self.repaint()
