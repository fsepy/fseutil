from PySide2 import QtWidgets, QtGui, QtCore

from fseutil.etc.images_base64 import dialog_0403_br187_parallel_figure_1 as figure_1
from fseutil.gui.layout.dialog_0403_br187_parallel_complex import Ui_MainWindow
from fseutil.lib.fse_thermal_radiation import phi_parallel_any_br187, linear_solver


class Dialog0403(QtWidgets.QMainWindow):
    maximum_acceptable_thermal_radiation_heat_flux = 12.6

    def __init__(self, parent=None):
        super(Dialog0403, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set up radiation figure
        ba = QtCore.QByteArray.fromBase64(figure_1)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.ui.label.setPixmap(pix_map)

        # set validators
        self.ui.lineEdit_W.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!')))
        self.ui.lineEdit_H.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!')))
        self.ui.lineEdit_w.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!')))
        self.ui.lineEdit_h.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!')))
        self.ui.lineEdit_Q.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!')))
        self.ui.lineEdit_S_or_UA.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!')))

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
        self.ui.lineEdit_w.setText('0')
        self.ui.lineEdit_h.setText('0')
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
        w = float(self.ui.lineEdit_w.text())
        h = float(self.ui.lineEdit_h.text())
        Q = float(self.ui.lineEdit_Q.text())

        q_target = self.maximum_acceptable_thermal_radiation_heat_flux

        # calculate start

        if self.ui.comboBox_S_or_UA.currentText() == '½S':  # to calculate maximum unprotected area
            # obtain separation distance
            S = float(self.ui.lineEdit_S_or_UA.text()) * 2
            S = max(1, min([S, 200]))
            self.ui.lineEdit_S_or_UA.setText(f'{S / 2:.2f}')

            # calculate view factor
            phi_solved = phi_parallel_any_br187(W_m=W, H_m=H, w_m=0.5 * W + w, h_m=0.5 * H + h, S_m=S)
            # calculate imposed thermal heat flux at receiver surface
            q_solved = Q * phi_solved
            # calculate maximum permissible unprotected area
            UA_solved = max([min([q_target / q_solved * 100, 100]), 0])

            # output results to ui
            self.ui.lineEdit_out_Phi.setText(f'{phi_solved:.4f}')
            self.ui.lineEdit_out_q.setText(f'{q_solved:.2f}')
            self.ui.lineEdit_out_S_or_UA.setText(f'{UA_solved:.2f}')

        elif self.ui.comboBox_S_or_UA.currentText() == 'UA':  # to calculate minimum separation distance to boundary
            # obtain unprotected area
            UA = float(self.ui.lineEdit_S_or_UA.text()) / 100.
            UA = max([0.0001, min([UA, 1])])
            self.ui.lineEdit_S_or_UA.setText(f'{UA * 100:.2f}')

            # Solve separation distance for target view factor, i.e. SOLVE `f(S) = phi` for `S` at `phi == phi_target`
            phi_target = q_target / (Q * UA)
            S_solved = linear_solver(
                func=phi_parallel_any_br187,
                dict_params=dict(W_m=W, H_m=H, w_m=0.5 * W + w, h_m=0.5 * H + h, S_m=0),
                x_name='S_m',
                y_target=phi_target,
                x_upper=200,
                x_lower=0.01,
                y_tol=0.001,
                iter_max=100,
                func_multiplier=-1
            )
            # calculate view factor for solved separation distance
            phi_solved = phi_parallel_any_br187(W_m=W, H_m=H, w_m=0.5 * W + w, h_m=0.5 * H + h, S_m=S_solved)
            # calculate imposed heat flux at receiver surface
            q_solved = Q * phi_solved

            # write results to ui
            self.ui.lineEdit_out_Phi.setText(f'{phi_solved:.4f}')
            self.ui.lineEdit_out_q.setText(f'{q_solved:.2f}')
            self.ui.lineEdit_out_S_or_UA.setText(f'{S_solved / 2:.2f}')

        self.repaint()
