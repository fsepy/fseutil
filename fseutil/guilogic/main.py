from PySide2 import QtWidgets, QtGui, QtCore

from fseutil.etc.images_base64 import OFR_LOGO_LARGE_PNG
from fseutil.etc.images_base64 import OFR_LOGO_SMALL_PNG
from fseutil.guilayout.main import Ui_MainWindow
from fseutil.guilogic.dialog_1_11_heat_detector_activation import Dialog0111_HeatDetectorActivation
from fseutil.guilogic.dialog_1_1_adb_datasheet_1 import Dialog0101_ADB2Datasheet1
from fseutil.guilogic.dialog_4_1_br187_parallel_simple import Dialog0401_br187ParallelSimple
from fseutil.guilogic.dialog_4_2_br187_perpendicular_simple import Dialog0402_br187PerpendicularSimple
from fseutil.guilogic.dialog_6_1_naming_convention import Dialog0601_NamingConvention


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_tabs()
        self.init_logos()
        self.init_buttons()

    def init_tabs(self):
        self.ui.action_0101_ADB_Vol_2_Datasheet.triggered.connect(self.activate_0101_adb2_datasheet_1)

    def init_logos(self):
        ba = QtCore.QByteArray.fromBase64(OFR_LOGO_SMALL_PNG)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.setWindowIcon(pix_map)

        ba = QtCore.QByteArray.fromBase64(OFR_LOGO_LARGE_PNG)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.ui.label_logo.setPixmap(pix_map)

    def init_buttons(self):
        self.ui.pushButton_0101_adb2_datasheet_1.clicked.connect(self.activate_0101_adb2_datasheet_1)
        self.ui.pushButton_0111_heat_detector_activation.clicked.connect(self.activate_0111_heat_detector_activation)
        self.ui.pushButton_0401_br187_parallel_simple.clicked.connect(self.activate_0401_br187_parallel_simple)
        self.ui.pushButton_0402_br187_perpendicular_simple.clicked.connect(self.activate_0402_br187_perpendicular_simple)
        self.ui.pushButton_0601_naming_convention.clicked.connect(self.activate_0601_naming_convention)

    @staticmethod
    def activate_app(app_):
        app_.show()
        app_.exec_()

    def activate_0401_br187_parallel_simple(self):
        self.activate_app(Dialog0401_br187ParallelSimple(self))

    def activate_0402_br187_perpendicular_simple(self):
        self.activate_app(Dialog0402_br187PerpendicularSimple(self))

    def activate_0101_adb2_datasheet_1(self):
        self.activate_app(Dialog0101_ADB2Datasheet1(self))

    def activate_0111_heat_detector_activation(self):
        self.activate_app(Dialog0111_HeatDetectorActivation(self))

    def activate_0601_naming_convention(self):
        self.activate_app(Dialog0601_NamingConvention(self))
