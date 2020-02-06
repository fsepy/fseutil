from PySide2 import QtWidgets

from fseutil.guilayout.dialog_0602_pd_7974_flame_height import Ui_Dialog
from fseutil.lib.pd_7974_1_2019 import eq_11_dimensionless_hrr_rectangular
from fseutil.lib.pd_7974_1_2019 import eq_12_dimensionless_hrr_line
from fseutil.lib.pd_7974_1_2019 import eq_5_dimensionless_hrr
from fseutil.lib.fse_flame_height_ import mean_flame_height_pd_7974


class Dialog0602(QtWidgets.QDialog):

    maximum_acceptable_thermal_radiation_heat_flux = 12.6

    def __init__(self, parent=None):

        # instantiate ui
        super(Dialog0602, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # set up figures
        # ba = QtCore.QByteArray.fromBase64(dialog_4_3_br187_parallel_figure_1)
        # pix_map = QtGui.QPixmap()
        # pix_map.loadFromData(ba)
        # self.ui.label.setPixmap(pix_map)

        # set default values
        # todo
        self.change_fire_shape()

        # signal and slots
        self.ui.comboBox_fire_shape.currentIndexChanged.connect(self.change_fire_shape)
        self.ui.pushButton_test.clicked.connect(self.test)
        self.ui.pushButton_calculate.clicked.connect(self.calculate)

    def change_fire_shape(self):
        if self.ui.comboBox_fire_shape.currentIndex() == 0:  # circular fire source
            self.ui.label_Q_dot_or_Q_dot_l.setText('Q_dot')
            self.ui.label_Q_dot_or_Q_dot_l_unit.setText('kW')
            self.ui.label_L_A_or_D.setText('D')
            self.ui.label_L_B.setDisabled(True)
            self.ui.lineEdit_L_B.setDisabled(True)
            self.ui.label_L_B_unit.setDisabled(True)
        elif self.ui.comboBox_fire_shape.currentIndex() == 1:  # rectangular fire source
            self.ui.label_Q_dot_or_Q_dot_l.setText('Q_dot')
            self.ui.label_Q_dot_or_Q_dot_l_unit.setText('kW')
            self.ui.label_L_A_or_D.setText(r'L<sub>A<\sub>')
            self.ui.label_L_B.setDisabled(False)
            self.ui.lineEdit_L_B.setDisabled(False)
            self.ui.label_L_B_unit.setDisabled(False)
        elif self.ui.comboBox_fire_shape.currentIndex() == 2:  # line fire source
            self.ui.label_Q_dot_or_Q_dot_l.setText('Q_dot_l')
            self.ui.label_Q_dot_or_Q_dot_l_unit.setText('kW/m')
            self.ui.label_L_A_or_D.setText(r'L<sub>A<\sub>')
            self.ui.label_L_B.setDisabled(True)
            self.ui.lineEdit_L_B.setDisabled(True)
            self.ui.label_L_B_unit.setDisabled(True)
        else:
            raise ValueError('Unknown fire shape.')

    def change_fuel_type(self):
        pass

    def test(self):
        self.ui.comboBox_fire_shape.setCurrentIndex(0)
        self.ui.comboBox_fuel_type.setCurrentIndex(0)
        self.ui.lineEdit_Q_dot_or_Q_dot_l.setText('1500')
        self.ui.lineEdit_L_A_or_D.setText('2.5')
        self.ui.lineEdit_rho_0.setText('1.2')
        self.ui.lineEdit_c_p_0.setText('1.0')
        self.ui.lineEdit_T_0.setText('293.15')
        self.ui.lineEdit_g.setText('9.81')

        self.repaint()

        self.calculate()

    def calculate(self):

        Q_dot_or_Q_dot_l = float(self.ui.lineEdit_Q_dot_or_Q_dot_l.text())
        L_A_or_D = float(self.ui.lineEdit_L_A_or_D.text())
        try:
            L_B = float(self.ui.lineEdit_L_B.text())
        except ValueError:
            L_B = None
        rho_0 = float(self.ui.lineEdit_rho_0.text())
        c_p_0 = float(self.ui.lineEdit_c_p_0.text())
        T_0 = float(self.ui.lineEdit_T_0.text())
        g = float(self.ui.lineEdit_g.text())
        fuel_type = int(self.ui.comboBox_fuel_type.currentIndex())

        if self.ui.comboBox_fire_shape.currentIndex() == 0:  # circular fire source
            Q_dot_star = eq_5_dimensionless_hrr(
                Q_dot_kW=Q_dot_or_Q_dot_l,
                rho_0=rho_0,
                c_p_0_kJ_kg_K=c_p_0,
                T_0=T_0,
                g=g,
                D=L_A_or_D,
            )
            flame_height = mean_flame_height_pd_7974(Q_dot_star=Q_dot_star, fuel_type=fuel_type, fire_diameter=L_A_or_D)
        elif self.ui.comboBox_fire_shape.currentIndex() == 1:  # rectangular fire source
            Q_dot_star = eq_11_dimensionless_hrr_rectangular(
                Q_dot_kW=Q_dot_or_Q_dot_l,
                rho_0=rho_0,
                c_p_0_kJ_kg_K=c_p_0,
                T_0=T_0,
                g=g,
                L_A=L_A_or_D,
                L_B=L_B
            )
            flame_height = mean_flame_height_pd_7974(
                Q_dot_star=Q_dot_star, fuel_type=fuel_type, fire_diameter=(L_A_or_D + L_B) / 2.
            )
        elif self.ui.comboBox_fire_shape.currentIndex() == 2:  # line fire source
            Q_dot_star = eq_12_dimensionless_hrr_line(
                Q_dot_l_kW_m=Q_dot_or_Q_dot_l,
                rho_0=rho_0,
                c_p_0_kJ_kg_K=c_p_0,
                T_0=T_0,
                g=g,
                L_A=L_A_or_D,
            )
            flame_height = mean_flame_height_pd_7974(
                Q_dot_star=Q_dot_star, fuel_type=fuel_type, fire_diameter=L_A_or_D
            )
        else:
            raise ValueError('Unknown fire shape.')

        self.ui.lineEdit_Q_dot_star.setText(f'{Q_dot_star:.2f}')
        self.ui.lineEdit_Z_f.setText(f'{flame_height:.2f}')

        self.repaint()
