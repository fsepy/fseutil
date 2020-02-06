import base64
import base64
import tempfile
import numpy as np

from PySide2 import QtWidgets, QtGui

from fseutil.etc.images_base64 import dialog_1_11_heat_detector_activation_figure_1
from fseutil.guilayout.dialog_1_11_heat_detector_activation import Ui_dialog_1_11_heat_detector_activation
from fseutil.lib.fse_activation_hd import heat_detector_temperature_pd7974
from fseutil.lib.pd_7974_1_2019 import eq_22_t_squared_fire_growth


class Dialog0111(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Dialog0111, self).__init__(parent)
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

        assert abs(float(self.ui.lineEdit_out_t_act.text()) - 237.5) <= 0.5

        self.repaint()

    def calculate(self):

        # get data
        t = float(self.ui.lineEdit_in_t.text())
        alpha = float(self.ui.lineEdit_in_alpha.text())
        detector_to_fire_vertical_distance = float(self.ui.lineEdit_in_H.text())
        detector_to_fire_horizontal_distance = float(self.ui.lineEdit_in_R.text())
        detector_response_time_index = float(self.ui.lineEdit_in_RTI.text())
        detector_conduction_factor = float(self.ui.lineEdit_in_C.text())
        fire_hrr_density_kWm2 = float(self.ui.lineEdit_in_HRRPUA.text())
        fire_convection_fraction = float(self.ui.lineEdit_in_C_conv.text())
        detector_activation_temperature = float(self.ui.lineEdit_in_T_act.text())

        # Code results
        t = [i * 0.5 for i in range(int(t))]
        res = heat_detector_temperature_pd7974(
            gas_time=t,
            gas_hrr_kWm2=[eq_22_t_squared_fire_growth(alpha, t=i) / 1000. for i in t],
            detector_to_fire_vertical_distance=detector_to_fire_vertical_distance,
            detector_to_fire_horizontal_distance=detector_to_fire_horizontal_distance,
            detector_response_time_index=detector_response_time_index,
            detector_conduction_factor=detector_conduction_factor,
            fire_hrr_density_kWm2=fire_hrr_density_kWm2,
            fire_convection_fraction=fire_convection_fraction,
        )

        for i, time in enumerate(t):
            jet_temperature = res['jet_temperature'][i]
            detector_temperature = res['detector_temperature'][i]
            if detector_temperature-273.15 >= detector_activation_temperature:
                self.ui.lineEdit_out_t_act.setText(f'{time:.1f}')
                # print(f'{time:5.1f} s, {jet_temperature - 273.15:10.1f} °C, {detector_temperature - 273.15:10.1f} °C')
                break

        self.repaint()
