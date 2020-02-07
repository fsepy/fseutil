import base64
import tempfile
import numpy as np

from PySide2 import QtWidgets, QtGui

from fseutil.etc.images_base64 import dialog_1_11_heat_detector_activation_figure_1
from fseutil.guilayout.dialog_0111_heat_detector_activation import Ui_dialog_1_11_heat_detector_activation
from fseutil.lib.fse_activation_hd import heat_detector_temperature_pd7974
from fseutil.libstd.pd_7974_1_2019 import eq_22_t_squared_fire_growth


class Dialog0111(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_dialog_1_11_heat_detector_activation()
        self.ui.setupUi(self)

        # set up radiation figure

        _, fp_image_1 = tempfile.mkstemp()
        with open(fp_image_1, "wb") as f:
            f.write(base64.b64decode(dialog_1_11_heat_detector_activation_figure_1))

        pixmap = QtGui.QPixmap(fp_image_1)
        self.ui.label.setPixmap(pixmap)

        self.ui.pushButton_calculate.clicked.connect(self.calculate)
        self.ui.pushButton_test.clicked.connect(self.test)

        self.parent().statusBar().showMessage('Hello from sub class.')

    def test(self):

        self.ui.lineEdit_in_t.setText('600')
        self.ui.lineEdit_in_alpha.setText('0.0117')
        self.ui.lineEdit_in_H.setText('2.4')
        self.ui.lineEdit_in_R.setText('2.75')
        self.ui.lineEdit_in_RTI.setText('115')
        self.ui.lineEdit_in_C.setText('0.4')
        self.ui.lineEdit_in_HRRPUA.setText('510')
        self.ui.lineEdit_in_C_conv.setText('0.67')
        self.ui.lineEdit_in_T_act.setText('58')

        self.calculate()

        # assert abs(float(self.ui.lineEdit_out_t_act.text()) - 237.5) <= 0.5

        self.repaint()

    def calculate(self):

        # clear outputs
        self.ui.lineEdit_out_t_act.setText('')

        # get data
        gas_time = float(self.ui.lineEdit_in_t.text())
        alpha = float(self.ui.lineEdit_in_alpha.text())
        detector_to_fire_vertical_distance = float(self.ui.lineEdit_in_H.text())
        detector_to_fire_horizontal_distance = float(self.ui.lineEdit_in_R.text())
        detector_response_time_index = float(self.ui.lineEdit_in_RTI.text())
        detector_conduction_factor = float(self.ui.lineEdit_in_C.text())
        fire_hrr_density_kWm2 = float(self.ui.lineEdit_in_HRRPUA.text())
        fire_convection_fraction = float(self.ui.lineEdit_in_C_conv.text())
        detector_activation_temperature = float(self.ui.lineEdit_in_T_act.text())

        # calculate all sorts of things
        gas_time = np.arange(0, gas_time, 1.)
        gas_hrr_kWm2 = eq_22_t_squared_fire_growth(alpha, gas_time) / 1000.
        res = heat_detector_temperature_pd7974(
            gas_time=gas_time,
            gas_hrr_kWm2=gas_hrr_kWm2,
            detector_to_fire_vertical_distance=detector_to_fire_vertical_distance,
            detector_to_fire_horizontal_distance=detector_to_fire_horizontal_distance,
            detector_response_time_index=detector_response_time_index,
            detector_conduction_factor=detector_conduction_factor,
            fire_hrr_density_kWm2=fire_hrr_density_kWm2,
            fire_convection_fraction=fire_convection_fraction,
        )

        # work out activation time
        activation_time = gas_time[np.argmin(np.abs((res['detector_temperature']-273.15) - detector_activation_temperature))]
        self.ui.lineEdit_out_t_act.setText(f'{activation_time:.1f}')

        # print results (for console enabled version only)
        for i, time in enumerate(gas_time):
            fire_hrr = gas_hrr_kWm2[i]
            detector_temperature = res['detector_temperature'][i]
            jet_velocity = res['jet_velocity'][i]
            jet_temperature = res['jet_temperature'][i]
            virtual_origin = res['virtual_origin'][i]
            print(f'{time:5.2f} s, {fire_hrr:10.2f} kW {virtual_origin:10.2f} m {jet_velocity:10.2f} m/s {jet_temperature - 273.15:10.2f} °C, {detector_temperature - 273.15:10.2f} °C')

        self.repaint()
