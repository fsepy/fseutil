import datetime

from PySide2 import QtWidgets, QtGui, QtCore

import fseutil
from fseutil.etc.images_base64 import OFR_LOGO_1_PNG
from fseutil.etc.images_base64 import OFR_LOGO_2_PNG
from fseutil.guilayout.main import Ui_MainWindow
from fseutil.guilogic.dialog_0001_pass_code import Dialog0001 as Dialog0001
from fseutil.guilogic.dialog_0101_adb_datasheet_1 import Dialog0101 as Dialog0101
from fseutil.guilogic.dialog_0102_bs9999_datasheet_1 import Dialog0102 as Dialog0102
from fseutil.guilogic.dialog_0111_heat_detector_activation import Dialog0111 as Dialog0111
from fseutil.guilogic.dialog_0401_br187_parallel_simple import Dialog0401 as Dialog0401
from fseutil.guilogic.dialog_0402_br187_perpendicular_simple import Dialog0402 as Dialog0402
from fseutil.guilogic.dialog_0403_br187_parallel_complex import Dialog0403 as Dialog0403
from fseutil.guilogic.dialog_0404_br187_perpendicular_complex import Dialog0404 as Dialog0404
from fseutil.guilogic.dialog_0601_naming_convention import Dialog0601 as Dialog0601
from fseutil.guilogic.dialog_0602_flame_height import Dialog0602 as Dialog0602


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('OFR Fire Safety Engineering Utility Tools')

        self.init_check_expiry_date()
        self.init_tabs()
        self.init_logos()
        self.init_buttons()

        self.ui.label_big_name.setText('FSEUTIL')
        self.ui.label_version.setText('Version ' + fseutil.__version__)

    def init_check_expiry_date(self):

        # check expiry date, whether the tool is over 180 days old
        expiry_date_duration = 30
        if datetime.datetime.now() > fseutil.__date_released__ + datetime.timedelta(days=expiry_date_duration):
            app_ = self.activate_app(Dialog0001)
            if app_.pass_code != '':
                raise ValueError('Incorrect password.')
            else:
                app_.close()

    def init_tabs(self):
        self.ui.action_0101_ADB_Vol_2_Datasheet.triggered.connect(lambda: self.activate_app(Dialog0101))

    def init_logos(self):
        ba = QtCore.QByteArray.fromBase64(OFR_LOGO_1_PNG)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.setWindowIcon(pix_map)

        ba = QtCore.QByteArray.fromBase64(OFR_LOGO_2_PNG)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.ui.label_logo.setPixmap(pix_map)

    def init_buttons(self):

        self.ui.pushButton_0101_adb2_datasheet_1.clicked.connect(lambda: self.activate_app(Dialog0101))
        self.ui.pushButton_0102_bs9999_datasheet_1.clicked.connect(lambda: self.activate_app(Dialog0102))
        self.ui.pushButton_0111_heat_detector_activation.clicked.connect(lambda: self.activate_app(Dialog0111))

        self.ui.pushButton_0401_br187_parallel_simple.clicked.connect(lambda: self.activate_app(Dialog0401))
        self.ui.pushButton_0402_br187_perpendicular_simple.clicked.connect(lambda: self.activate_app(Dialog0402))
        self.ui.pushButton_0403_br187_parallel_complex.clicked.connect(lambda: self.activate_app(Dialog0403))
        self.ui.pushButton_0404_br187_perpendicular_complex.clicked.connect(lambda: self.activate_app(Dialog0404))

        self.ui.pushButton_0601_naming_convention.clicked.connect(lambda: self.activate_app(Dialog0601))
        self.ui.pushButton_0602_pd7974_flame_height.clicked.connect(lambda: self.activate_app(Dialog0602))

    def activate_app(self, app_):
        app_ = app_(self)
        app_.show()
        app_.exec_()
        return app_
