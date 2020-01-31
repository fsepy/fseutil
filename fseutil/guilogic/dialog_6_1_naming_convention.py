from PySide2 import QtWidgets
from fseutil.guilayout.dialog_6_1_naming_convention import Ui_dialog_6_1_naming_convention


class Dialog0601_NamingConvention(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dialog0601_NamingConvention, self).__init__(parent)
        self.ui = Ui_dialog_6_1_naming_convention()
        self.ui.setupUi(self)

    def update_file_full_name(self):
        # self.ui.label_out
        pass
