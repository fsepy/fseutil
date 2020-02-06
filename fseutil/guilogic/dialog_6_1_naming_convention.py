from PySide2 import QtWidgets, QtCore, QtGui
from fseutil.guilayout.dialog_6_1_naming_convention import Ui_dialog_6_1_naming_convention
from datetime import datetime


class Dialog0601(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dialog0601, self).__init__(parent)
        self.ui = Ui_dialog_6_1_naming_convention()
        self.ui.setupUi(self)

        self.ui.lineEdit_1_date.setText(datetime.today().strftime('%Y%m%d')[2:])

        self.make_file_name()

        self.ui.lineEdit_1_date.textChanged.connect(self.make_file_name)
        self.ui.comboBox_2_revision.currentTextChanged.connect(self.make_file_name)
        self.ui.lineEdit_3_project_no.textChanged.connect(self.make_file_name)
        self.ui.lineEdit_4_project_stage.textChanged.connect(self.make_file_name)
        self.ui.lineEdit_5_title.textChanged.connect(self.make_file_name)
        self.ui.comboBox_6_type.currentTextChanged.connect(self.make_file_name)
        self.ui.comboBox_7_security_status.currentTextChanged.connect(self.make_file_name)

        self.ui.pushButton_copy.clicked.connect(self.copy_file_name)

        self.repaint()

    def make_file_name(self):
        aa = self.ui.lineEdit_1_date.text()
        bb = self.ui.comboBox_2_revision.currentText()[0:3]
        cc = self.ui.lineEdit_3_project_no.text()
        dd = self.ui.lineEdit_4_project_stage.text()
        ee = self.ui.lineEdit_5_title.text()
        ff = self.ui.comboBox_6_type.currentText()[0:2]
        gg = self.ui.comboBox_7_security_status.currentText()[0:3]

        self.ui.lineEdit_result.setText('-'.join([aa, bb, cc, dd, ee, ff, gg]))

    def copy_file_name(self):
        clipboard = QtGui.QGuiApplication.clipboard()
        clipboard.setText(self.ui.lineEdit_result.text())
        self.ui.lineEdit_result.selectAll()
