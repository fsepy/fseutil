import base64
import tempfile

import numpy as np
from PySide2 import QtWidgets, QtGui, QtCore

from fseutil.etc.images_base64 import dialog_0111_heat_detector_activation_figure_1
from fseutil.gui.layout.dialog_0111_heat_detector_activation import Ui_MainWindow as Ui_Dialog
from fseutil.lib.fse_activation_hd import heat_detector_temperature_pd7974
from fseutil.libstd.pd_7974_1_2019 import eq_22_t_squared_fire_growth


class Dialog0111(QtWidgets.QMainWindow):

    _results = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # default values
        self.set_plume_temperature_correlation(False)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(QtCore.QByteArray.fromBase64(dialog_0111_heat_detector_activation_figure_1))
        self.ui.label.setPixmap(pixmap)

        # signals
        self.ui.checkBox_option_use_plume_temperature.stateChanged.connect(
            lambda x=self.ui.checkBox_option_use_plume_temperature.isChecked(): self.set_plume_temperature_correlation(x)
        )
        self.ui.pushButton_calculate.clicked.connect(self.calculate)
        self.ui.pushButton_test.clicked.connect(self.test)

        self.parent().statusBar().showMessage('Hello from sub class.')

    def set_plume_temperature_correlation(self, val):
        self.ui.checkBox_option_use_plume_temperature.setChecked(val)
        if val:
            self.ui.lineEdit_in_R.setEnabled(False)
        else:
            self.ui.lineEdit_in_R.setEnabled(True)

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
        time = float(self.ui.lineEdit_in_t.text())
        alpha = float(self.ui.lineEdit_in_alpha.text())
        detector_to_fire_vertical_distance = float(self.ui.lineEdit_in_H.text())
        try:  # `detector_to_fire_horizontal_distance` may be disabled if plume temperature correlation is checked.
            detector_to_fire_horizontal_distance = float(self.ui.lineEdit_in_R.text())
        except ValueError:
            detector_to_fire_horizontal_distance = 0.
        detector_response_time_index = float(self.ui.lineEdit_in_RTI.text())
        detector_conduction_factor = float(self.ui.lineEdit_in_C.text())
        fire_hrr_density_kWm2 = float(self.ui.lineEdit_in_HRRPUA.text())
        fire_convection_fraction = float(self.ui.lineEdit_in_C_conv.text())
        detector_activation_temperature = float(self.ui.lineEdit_in_T_act.text())

        # calculate all sorts of things
        time = np.arange(0, time, 1.)
        gas_hrr_kW = eq_22_t_squared_fire_growth(alpha, time) / 1000.
        res = heat_detector_temperature_pd7974(
            gas_time=time,
            gas_hrr_kW=gas_hrr_kW,
            detector_to_fire_vertical_distance=detector_to_fire_vertical_distance,
            detector_to_fire_horizontal_distance=detector_to_fire_horizontal_distance,
            detector_response_time_index=detector_response_time_index,
            detector_conduction_factor=detector_conduction_factor,
            fire_hrr_density_kWm2=fire_hrr_density_kWm2,
            fire_convection_fraction=fire_convection_fraction,
            force_plume_temperature_correlation=self.ui.checkBox_option_use_plume_temperature.isChecked()
        )
        res['time'], res['gas_hrr_kW'] = time, gas_hrr_kW

        # work out activation time
        activation_time = time[
            np.argmin(np.abs((res['detector_temperature'] - 273.15) - detector_activation_temperature))]
        self.ui.lineEdit_out_t_act.setText(f'{activation_time:.1f}')

        # print results (for console enabled version only)
        list_title = ['Time', 'HRR', 'V. Origin', 'Jet T.', 'Jet Vel.', 'Detector T.']
        list_param = ['time', 'gas_hrr_kW', 'virtual_origin', 'jet_temperature', 'jet_velocity', 'detector_temperature']
        list_units = ['s', 'kW', 'm', '°C', 'm/s', '°C']
        for i, time_ in enumerate(time):
            fs1_ = list()
            for i_, param in enumerate(list_param):
                v = res[param][i]
                unit = list_units[i_]
                fs1_.append('{:<15.14}'.format(f'{v:<.2f} {unit:<}'))

            if i % 25 == 0:
                print('\n'+''.join(f'{i_:<15.15}' for i_ in list_title))
            print(''.join(fs1_))

        # store calculated results
        self._results = res

        self.repaint()
