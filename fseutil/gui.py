# !/usr/bin/python
# coding:utf-8

import sys
import base64
import tempfile
from PySide2 import QtCore, QtWidgets, QtGui
from fseutil.ui.main import Ui_MainWindow
from fseutil.ui.dialog_4_1_br187_parallel_simple import Ui_dialog_4_1_br187_parallel_simple
from fseutil.ui.dialog_1_1_adb_datasheet_1 import Ui_dialog_1_1_adb_datasheet_1
from fseutil.ui.dialog_6_1_naming_convention import Ui_dialog_6_1_naming_convention
from fseutil.ui.dialog_1_11_heat_detector_activation import Ui_dialog_1_11_heat_detector_activation
from fseutil.etc.images_base64 import OFR_LOGO_LARGE_PNG_BASE64
from fseutil.etc.images_base64 import dialog_4_1_br187_parallel_figure_1
from fseutil.etc.images_base64 import dialog_4_2_br187_perpendicular_figure_1
from fseutil.etc.images_base64 import dialog_1_1_adb2_datasheet_1
from fseutil.etc.images_base64 import dialog_1_11_heat_detector_activation_figure_1
from fseutil.lib.fse_thermal_radiation import phi_parallel_any_br187, phi_perpendicular_any_br187, linear_solver
from fseutil.lib.pd_7974_1_2019 import eq_22_t_squared_fire_growth
from fseutil.lib.fse_activation_hd import heat_detector_temperature_pd7974


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        _, fp_image_1 = tempfile.mkstemp()
        with open(fp_image_1, "wb") as f:
            f.write(base64.b64decode(OFR_LOGO_LARGE_PNG_BASE64))

        pixmap = QtGui.QPixmap(fp_image_1)
        self.ui.label_logo.setPixmap(pixmap)

        self.ui.pushButton_0101_adb2_datasheet_1.clicked.connect(self.activate_0101_adb2_datasheet_1)
        self.ui.pushButton_0111_heat_detector_activation.clicked.connect(self.activate_0111_heat_detector_activation)
        self.ui.pushButton_0401_br187_parallel_simple.clicked.connect(self.activate_0401_br187_parallel_simple)
        self.ui.pushButton_0402_br187_perpendicular_simple.clicked.connect(self.activate_0402_br187_perpendicular_simple)

    def activate_0401_br187_parallel_simple(self):
        app = Dialog0401_br187ParallelSimple(self)
        app.show()
        app.exec_()

    def activate_0402_br187_perpendicular_simple(self):
        app = Dialog0402_br187PerpendicularSimple(self)
        app.show()
        app.exec_()

    def activate_0101_adb2_datasheet_1(self):
        app = Dialog0101_ADB2Datasheet1(self)
        app.show()
        app.exec_()

    def activate_0111_heat_detector_activation(self):
        app = Dialog0111_HeatDetectorActivation(self)
        app.show()
        app.exec_()


class Dialog0401_br187ParallelSimple(QtWidgets.QDialog):

    maximum_acceptable_thermal_radiation_heat_flux = 12.6

    def __init__(self, parent=None):
        super(Dialog0401_br187ParallelSimple, self).__init__(parent)
        self.ui = Ui_dialog_4_1_br187_parallel_simple()
        self.ui.setupUi(self)

        # set up radiation figure

        _, fp_image_1 = tempfile.mkstemp()
        with open(fp_image_1, "wb") as f:
            f.write(base64.b64decode(dialog_4_1_br187_parallel_figure_1))

        pixmap = QtGui.QPixmap(fp_image_1)
        self.ui.label.setPixmap(pixmap)

        self.ui.comboBox_S_or_UA.currentTextChanged.connect(self.change_mode_S_and_UA)
        self.ui.pushButton_calculate.clicked.connect(self.calculate)
        self.ui.pushButton_test.clicked.connect(self.test)

    def change_mode_S_and_UA(self):
        """update ui to align with whether to calculate boundary distance or unprotected area %"""
        
        # change input and output labels and units
        if self.ui.comboBox_S_or_UA.currentText() == '½S':  # to calculate separation to boundary
            self.ui.label_unit_S_or_UA.setText('m')
            self.ui.label_out_S_or_UA.setText('UA')
            self.ui.label_out_unit_S_or_UA.setText('%')
            self.ui.label_out_S_or_UA.setToolTip('Maximum permissible unprotected area')

        elif self.ui.comboBox_S_or_UA.currentText() == 'UA':  # to calculate unprotected area percentage
            self.ui.label_unit_S_or_UA.setText('%')
            self.ui.label_out_S_or_UA.setText('½S')
            self.ui.label_out_unit_S_or_UA.setText('m')
            self.ui.label_out_S_or_UA.setToolTip('Separation distance from emitter to notional boundary')
        else:
            raise ValueError('Unknown value for input UA or S.')

        # clear outputs
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')
        self.ui.lineEdit_out_S_or_UA.setText('')

        self.repaint()

    def test(self):

        self.ui.lineEdit_W.setText('10')
        self.ui.lineEdit_H.setText('10')
        self.ui.lineEdit_Q.setText('84')
        self.ui.comboBox_S_or_UA.setCurrentIndex(0)
        self.change_mode_S_and_UA()
        self.ui.lineEdit_S_or_UA.setText('2')

        self.calculate()

        self.repaint()

    def calculate(self):

        # clear ui output fields

        self.ui.lineEdit_out_S_or_UA.setText('')
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')

        # parse inputs from ui

        W=float(self.ui.lineEdit_W.text())
        H=float(self.ui.lineEdit_H.text())
        Q=float(self.ui.lineEdit_Q.text())

        # calculate

        q_target = self.maximum_acceptable_thermal_radiation_heat_flux

        if self.ui.comboBox_S_or_UA.currentText() == '½S':  # to calculate maximum unprotected area
            S = float(self.ui.lineEdit_S_or_UA.text()) * 2
            S = max(1, min([S, 200]))
            self.ui.lineEdit_S_or_UA.setText(f'{S/2:.2f}')

            phi_solved = phi_parallel_any_br187(W_m=W, H_m=H, w_m=0.5*W, h_m=0.5*H, S_m=S)
            q_solved = Q * phi_solved
            UA_solved = max([min([q_target/q_solved * 100, 100]), 0])

            self.ui.lineEdit_out_Phi.setText(f'{phi_solved:.4f}')
            self.ui.lineEdit_out_q.setText(f'{q_solved:.2f}')
            self.ui.lineEdit_out_S_or_UA.setText(f'{UA_solved:.2f}')

        elif self.ui.comboBox_S_or_UA.currentText() == 'UA':  # to calculate minimum separation distance to boundary
            UA = float(self.ui.lineEdit_S_or_UA.text()) / 100.
            UA = max([0.0001, min([UA, 1])])
            self.ui.lineEdit_S_or_UA.setText(f'{UA*100:.0f}')

            phi_target = q_target/(Q*UA)
            S_solved = linear_solver(
                func=phi_parallel_any_br187,
                dict_params=dict(W_m=W, H_m=H, w_m=0.5*W, h_m=0.5*H, S_m=0),
                x_name='S_m',
                y_target=phi_target,
                x_upper=200,
                x_lower=0.01,
                y_tol=0.001,
                iter_max=100,
                func_multiplier=-1
            )
            phi_solved = phi_parallel_any_br187(W_m=W, H_m=H, w_m=0.5*W, h_m=0.5*H, S_m=S_solved)
            q_solved = Q * phi_solved

            self.ui.lineEdit_out_Phi.setText(f'{phi_solved:.4f}')
            self.ui.lineEdit_out_q.setText(f'{q_solved:.2f}')
            self.ui.lineEdit_out_S_or_UA.setText(f'{S_solved/2:.2f}')

            self.repaint()


class Dialog0402_br187PerpendicularSimple(QtWidgets.QDialog):

    maximum_acceptable_thermal_radiation_heat_flux = 12.6

    def __init__(self, parent=None):
        super(Dialog0402_br187PerpendicularSimple, self).__init__(parent)
        self.ui = Ui_dialog_4_1_br187_parallel_simple()
        self.ui.setupUi(self)

        # set up radiation figure

        _, fp_image_1 = tempfile.mkstemp()
        with open(fp_image_1, "wb") as f:
            f.write(base64.b64decode(dialog_4_2_br187_perpendicular_figure_1))

        pixmap = QtGui.QPixmap(fp_image_1)
        self.ui.label.setPixmap(pixmap)

        self.ui.comboBox_S_or_UA.currentTextChanged.connect(self.change_mode_S_and_UA)
        self.ui.pushButton_calculate.clicked.connect(self.calculate)
        self.ui.pushButton_test.clicked.connect(self.test)

    def test(self):

        self.ui.lineEdit_W.setText('50')
        self.ui.lineEdit_H.setText('50')
        self.ui.lineEdit_Q.setText('84')
        self.ui.comboBox_S_or_UA.setCurrentIndex(0)
        self.change_mode_S_and_UA()
        self.ui.lineEdit_S_or_UA.setText('2')

        self.calculate()

        self.repaint()

    def change_mode_S_and_UA(self):
        """update ui to align with whether to calculate boundary distance or unprotected area %"""

        # change input and output labels and units
        if self.ui.comboBox_S_or_UA.currentText() == '½S':  # to calculate separation to boundary
            self.ui.label_unit_S_or_UA.setText('m')
            self.ui.label_out_S_or_UA.setText('UA')
            self.ui.label_out_unit_S_or_UA.setText('%')
            self.ui.label_out_S_or_UA.setToolTip('Maximum permissible unprotected area')

        elif self.ui.comboBox_S_or_UA.currentText() == 'UA':  # to calculate unprotected area percentage
            self.ui.label_unit_S_or_UA.setText('%')
            self.ui.label_out_S_or_UA.setText('½S')
            self.ui.label_out_unit_S_or_UA.setText('m')
            self.ui.label_out_S_or_UA.setToolTip('Separation distance from emitter to notional boundary')
        else:
            raise ValueError('Unknown value for input UA or S.')

        # clear outputs
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')
        self.ui.lineEdit_out_S_or_UA.setText('')

        self.repaint()

    def calculate(self):

        # clear ui output fields

        self.ui.lineEdit_out_S_or_UA.setText('')
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')

        # parse inputs from ui

        W = float(self.ui.lineEdit_W.text())
        H = float(self.ui.lineEdit_H.text())
        Q = float(self.ui.lineEdit_Q.text())

        # calculate

        q_target = self.maximum_acceptable_thermal_radiation_heat_flux

        if self.ui.comboBox_S_or_UA.currentText() == '½S':  # to calculate maximum unprotected area
            S = float(self.ui.lineEdit_S_or_UA.text()) * 2
            S = max(1, min([S, 200]))
            self.ui.lineEdit_S_or_UA.setText(f'{S/2:.2f}')

            phi_solved = phi_perpendicular_any_br187(W_m=W, H_m=H, w_m=0., h_m=0., S_m=S)
            q_solved = Q * phi_solved
            UA_solved = max([min([q_target/q_solved * 100, 100]), 0])

            self.ui.lineEdit_out_Phi.setText(f'{phi_solved:.4f}')
            self.ui.lineEdit_out_q.setText(f'{q_solved:.2f}')
            self.ui.lineEdit_out_S_or_UA.setText(f'{UA_solved:.2f}')

        # to calculate minimum separation distance to boundary
        elif self.ui.comboBox_S_or_UA.currentText() == 'UA':
            UA = float(self.ui.lineEdit_S_or_UA.text()) / 100.
            UA = max([0.0001, min([UA, 1])])
            self.ui.lineEdit_S_or_UA.setText(f'{UA*100:.2f}')

            phi_target = q_target/(Q*UA)
            S_solved = linear_solver(
                func=phi_perpendicular_any_br187,
                dict_params=dict(W_m=W, H_m=H, w_m=0., h_m=0., S_m=0),
                x_name='S_m',
                y_target=phi_target,
                x_upper=1000,
                x_lower=0.01,
                y_tol=0.001,
                iter_max=500,
                func_multiplier=-1
            )
            phi_solved = phi_perpendicular_any_br187(W_m=W, H_m=H, w_m=0.5*W, h_m=0.5*H, S_m=S_solved)
            q_solved = Q * phi_solved

            self.ui.lineEdit_out_Phi.setText(f'{phi_solved:.4f}')
            self.ui.lineEdit_out_q.setText(f'{q_solved:.2f}')
            self.ui.lineEdit_out_S_or_UA.setText(f'{S_solved/2:.2f}')
        
        self.repaint()


class Dialog0101_ADB2Datasheet1(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dialog0101_ADB2Datasheet1, self).__init__(parent)
        self.ui = Ui_dialog_1_1_adb_datasheet_1()
        self.ui.setupUi(self)

        _, fp_image_1 = tempfile.mkstemp()
        with open(fp_image_1, "wb") as f:
            f.write(base64.b64decode(dialog_1_1_adb2_datasheet_1))

        pixmap = QtGui.QPixmap(fp_image_1)
        self.ui.label.setPixmap(pixmap)


class Dialog0111_HeatDetectorActivation(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Dialog0111_HeatDetectorActivation, self).__init__(parent)
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


class Dialog0601_NamingConvention(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dialog0601_NamingConvention, self).__init__(parent)
        self.ui = Ui_dialog_6_1_naming_convention()
        self.ui.setupUi(self)

    def update_file_full_name(self):
        # self.ui.label_out
        pass
    

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
