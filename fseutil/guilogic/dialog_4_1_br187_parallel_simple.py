from PySide2 import QtWidgets, QtGui, QtCore

from fseutil.etc.images_base64 import dialog_4_1_br187_parallel_figure_1
from fseutil.guilayout.dialog_0401_br187_parallel_simple import Ui_Dialog
from fseutil.lib.fse_thermal_radiation import phi_parallel_any_br187, linear_solver


class Dialog0401(QtWidgets.QDialog):

    maximum_acceptable_thermal_radiation_heat_flux = 12.6

    def __init__(self, parent=None):
        super(Dialog0401, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # set up radiation figure
        ba = QtCore.QByteArray.fromBase64(dialog_4_1_br187_parallel_figure_1)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.ui.label.setPixmap(pix_map)

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

        W = float(self.ui.lineEdit_W.text())
        H = float(self.ui.lineEdit_H.text())
        Q = float(self.ui.lineEdit_Q.text())

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
            self.ui.lineEdit_S_or_UA.setText(f'{UA*100:.2f}')

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
