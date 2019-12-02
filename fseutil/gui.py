import base64
import tempfile
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import typing
from fseutil import __version__ as _ver

from fseutil.lib.fse_b4_br187 import phi_parallel_any_br187, phi_perpendicular_any_br187
from fseutil.etc.b4_br187 import OFR_LOGO_LARGE_PNG_BASE64, OFR_LOGO_SMALL_PNG_BASE64
from fseutil.etc.b4_br187 import PARALLEL_LARGE_FIGURE_PNG_BASE64, PERPENDICULAR_LARGE_FIGURE_PNG_BASE64
from typing import Callable


def linear_solver(func: Callable, dict_params: dict, x_name: str, y_target: float, x_upper: float, x_lower: float, y_tol: float, iter_max: int = 1000, func_multiplier: float = 1):

    if x_lower > x_upper:
        x_lower += x_upper
        x_upper = x_lower - x_upper
        x_lower = x_lower - x_upper

    y_target *= func_multiplier

    x1 = x_lower
    x2 = (x_lower + x_upper) / 2
    x3 = x_upper

    dict_params[x_name] = x1
    y1 = func_multiplier * func(**dict_params)
    dict_params[x_name] = x2
    y2 = func_multiplier * func(**dict_params)
    dict_params[x_name] = x3
    y3 = func_multiplier * func(**dict_params)

    if y_target < y1:
        return None
    if y_target > y3:
        return None

    iter_count = 0
    while True:
        if abs(y2 - y_target) < y_tol:
            return x2
        elif iter_max < iter_count:
            return None
        elif y2 < y_target:
            x1 = x2
        elif y2 > y_target:
            x3 = x2
        x2 = (x1 + x3) / 2
        dict_params[x_name] = x2
        y2 = func_multiplier * func(**dict_params)
        iter_count += 1


class Messenger(tk.Tk):
    def __init__(self, msg, title=None):
        tk.Tk.__init__(self)

        title = "" if title is None else title
        self.wm_title(title)
        label = ttk.Label(self, text=msg, font=("Helvetica", 10))
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(self, text="OK", command=self.destroy)
        B1.pack()
        self.mainloop()


class Calculator(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.notebook = ttk.Notebook()

        # General App Setting
        # ===================
        self.app_name = "B4 BR187 Calculator"  # app name
        self.app_version = _ver  # app version

        self.init_ui()

        self.notebook.grid(row=0)

    def init_ui(self):

        # SETTINGS
        # ========

        # set window icon
        _, fp_icon = tempfile.mkstemp()
        with open(fp_icon, "wb") as f:
            f.write(base64.b64decode(OFR_LOGO_SMALL_PNG_BASE64))
        self.notebook.master.iconbitmap(fp_icon)
        # self.master.iconbitmap(fp_icon)

        self.notebook.master.title(self.app_name)

        # STYLES
        # ======

        style = ttk.Style()
        style.configure(
            "TLabel",
            foreground="black",
            background=self.notebook.master.cget("bg"),
            font=("Helvetica", 9),
        )
        style.configure(
            "TCheckbutton",
            foreground="black",
            background=self.notebook.master.cget("bg"),
            font=("Helvetica", 9),
        )
        self.columnconfigure(0, pad=10)
        self.rowconfigure(0, pad=10)

        self.tab_parallel = CalculatorParallelPanels(self.notebook)
        self.tab_perpendicular = CalculatorPerpendicularPanels(self.notebook)

        self.notebook.add(self.tab_parallel, text='Parallel Panels', compound=tk.TOP)
        self.notebook.add(self.tab_perpendicular, text='Perpendicular Panels', compound=tk.TOP)

        self.bind(sequence="<Return>", func=self.key_bind_enter)

    def key_bind_enter(self, _=None):
        if 'parallel' in str(self.notebook.tab(self.notebook.select(), "text")).lower():
            self.tab_parallel.calculate_resultant_heat_flux()
        elif 'perpendicular' in str(self.notebook.tab(self.notebook.select(), "text")).lower():
            self.tab_perpendicular.calculate_resultant_heat_flux()


class CalculatorParallelPanels(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # General App Setting
        # ===================
        self.app_name = "B4 BR187 Calculator"  # app name
        self.app_version = _ver  # app version
        self.app_description = """
        Thermal radiation calculator\nemitter and receiver pair\nin parallel.
        """
        # self.app_description = """
        # Thermal radiation calculator\nemitter and receiver pair\nin parallel.
        # """

        self.init_ui()

        self._check_center_receiver()
        self._check_to_boundary()
        self._check_solve_separation()
        self._check_solve_UA()

    def init_ui(self):

        # GUI LAYOUT
        # ==========

        # Large logo
        # ----------
        _, fp_radiation_figure_image = tempfile.mkstemp()
        with open(fp_radiation_figure_image, "wb") as f:
            f.write(base64.b64decode(OFR_LOGO_LARGE_PNG_BASE64))

        label_logo_image = Image.open(os.path.realpath(fp_radiation_figure_image))
        label_logo_image = label_logo_image.resize(
            (100, int(100 / 2.43)), Image.ANTIALIAS
        )
        label_logo_image = ImageTk.PhotoImage(label_logo_image)
        label_lage_logo = ttk.Label(self, image=label_logo_image)
        label_lage_logo.image = label_logo_image
        label_lage_logo.grid(row=0, column=1, rowspan=4, columnspan=2, sticky="ne", padx=(0, 5), pady=(10, 0))

        # Short description
        # -----------------
        txt = '\n'.join([self.app_description.strip(), self.app_version])
        label_description = ttk.Label(self, text=txt, anchor="nw", foreground="grey")
        label_description.grid(row=0, column=0, rowspan=4, sticky="nw", padx=(10, 0), pady=(10, 0))

        # Radiation figure
        # ----------------
        _, fp_logo_image = tempfile.mkstemp()
        with open(fp_logo_image, "wb") as f:
            f.write(base64.b64decode(PARALLEL_LARGE_FIGURE_PNG_BASE64))

        label_logo_image = Image.open(os.path.realpath(fp_logo_image))
        label_logo_image = label_logo_image.resize(
            (300, int(300 * 1.04689)), Image.ANTIALIAS
        )
        label_logo_image = ImageTk.PhotoImage(label_logo_image)
        self.label_lage_logo = ttk.Label(self, image=label_logo_image)
        self.label_lage_logo.image = label_logo_image
        self.label_lage_logo.grid(row=2, rowspan=16, column=0, columnspan=3, padx=10, pady=10)

        # Create Objects
        # ==============

        # Frames
        # ------

        self.labelframe_options = ttk.Labelframe(self, text="Options")
        self.labelframe_options.grid(row=0, column=3, rowspan=3, columnspan=3, sticky='we', padx=5, pady=5, ipadx=5, ipady=5)
        self.labelframe_inputs = ttk.Labelframe(self, text="Inputs")
        self.labelframe_inputs.grid(row=3, column=3, rowspan=6, columnspan=3, sticky='we', padx=5, pady=5, ipadx=5, ipady=5)
        self.labelframe_outputs = ttk.Labelframe(self, text="Outputs")
        self.labelframe_outputs.grid(row=9, column=3, rowspan=3, columnspan=3, sticky='we', padx=5, pady=5, ipadx=5, ipady=5)

        # Options
        # -------

        self.checkbutton_centered_v = tk.IntVar(value=1)  # set default, receiver to the center of emitter
        self.checkbutton_centered = ttk.Checkbutton(self.labelframe_options, text="Centered receiver", variable=self.checkbutton_centered_v, command=self._check_center_receiver)
        self.checkbutton_to_boundary_v = tk.IntVar(value=1)  # set default, separation to notional boundary
        self.checkbutton_to_boundary = ttk.Checkbutton(self.labelframe_options, text="Separation to boundary", variable=self.checkbutton_to_boundary_v, command=self._check_to_boundary)
        self.checkbutton_solve_separation_v = tk.IntVar(value=1)
        self.checkbutton_solve_separation = ttk.Checkbutton(self.labelframe_options, text="Solve separation", variable=self.checkbutton_solve_separation_v, command=self._check_solve_separation)
        self.checkbutton_solve_UA_v = tk.IntVar(value=1)
        self.checkbutton_solve_UA = ttk.Checkbutton(self.labelframe_options, text="Solve unprotected area", variable=self.checkbutton_solve_UA_v, command=self._check_solve_UA)
        self.list_options = [
            self.checkbutton_centered, self.checkbutton_to_boundary, self.checkbutton_solve_separation, self.checkbutton_solve_UA,
        ]

        # Inputs
        # ------

        self.label_W = ttk.Label(self.labelframe_inputs, text="W, emitter width")
        self.label_H = ttk.Label(self.labelframe_inputs, text="H, emitter height")
        self.label_Q1 = ttk.Label(self.labelframe_inputs, text="Q1, emitter HT (84, 168)")
        self.label_m = ttk.Label(self.labelframe_inputs, text="m, receiver loc. 1")
        self.label_n = ttk.Label(self.labelframe_inputs, text="n, receiver loc. 2")
        self.label_Q2 = ttk.Label(self.labelframe_inputs, text="Q2, receiver critical HT (12.6)")
        self.label_S = ttk.Label(self.labelframe_inputs, text="S, separation")
        self.label_UA = ttk.Label(self.labelframe_inputs, text="UA to solve separation")
        self.list_inputs_labels = [
            self.label_W, self.label_H, self.label_Q1,
            self.label_m, self.label_n, self.label_Q2,
            self.label_S, self.label_UA
        ]

        self.entry_W = ttk.Entry(self.labelframe_inputs)
        self.entry_H = ttk.Entry(self.labelframe_inputs)
        self.entry_Q1 = ttk.Entry(self.labelframe_inputs)
        self.entry_m = ttk.Entry(self.labelframe_inputs)
        self.entry_n = ttk.Entry(self.labelframe_inputs)
        self.entry_Q2 = ttk.Entry(self.labelframe_inputs)
        self.entry_S = ttk.Entry(self.labelframe_inputs)
        self.entry_UA = ttk.Entry(self.labelframe_inputs)
        self.list_inputs_entries = [
            self.entry_W, self.entry_H, self.entry_Q1,
            self.entry_m, self.entry_n, self.entry_Q2,
            self.entry_S, self.entry_UA
        ]

        self.label_W_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_H_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_Q1_unit = ttk.Label(self.labelframe_inputs, text="kW/m²")
        self.label_m_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_n_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_Q2_unit = ttk.Label(self.labelframe_inputs, text="kW/m²")
        self.label_S_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_UA_unit = ttk.Label(self.labelframe_inputs, text='%')
        self.list_inputs_units = [
            self.label_W_unit, self.label_H_unit, self.label_Q1_unit,
            self.label_m_unit, self.label_n_unit, self.label_Q2_unit,
            self.label_S_unit, self.label_UA_unit
        ]

        # Outputs
        # -------

        self.label_Q2r = ttk.Label(self.labelframe_outputs, text="Solved Q2 for 100% UA")
        self.label_Sr = ttk.Label(self.labelframe_outputs, text="Solved separation S")
        self.label_UAr = ttk.Label(self.labelframe_outputs, text="Solved UA")
        self.list_outputs_labels = [
            self.label_Q2r, self.label_Sr, self.label_UAr
        ]
        self.entry_Q2r = ttk.Entry(self.labelframe_outputs)
        self.entry_Sr = ttk.Entry(self.labelframe_outputs)
        self.entry_UAr = ttk.Entry(self.labelframe_outputs)
        self.list_outputs_entries = [
            self.entry_Q2r, self.entry_Sr, self.entry_UAr
        ]
        self.label_Q2r_unit = ttk.Label(self.labelframe_outputs, text="kW/m²")
        self.label_Sr_unit = ttk.Label(self.labelframe_outputs, text="m")
        self.label_UAr_unit = ttk.Label(self.labelframe_outputs, text="%")
        self.list_outputs_units = [
            self.label_Q2r_unit, self.label_Sr_unit, self.label_UAr_unit
        ]

        # Set Grid Location
        # -----------------

        for i, v in enumerate(self.list_options):
            v.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            # v.config(width=25)

        for i, v in enumerate(self.list_inputs_labels):
            v.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            v.config(width=25)
        for i, v in enumerate(self.list_inputs_entries):
            v.grid(row=i, column=1, sticky="w", padx=5, pady=1)
            v.config(width=10)
        for i, v in enumerate(self.list_inputs_units):
            v.grid(row=i, column=2, sticky="w", padx=5, pady=1)
            v.config(width=5)

        for i, v in enumerate(self.list_outputs_labels):
            v.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            v.config(width=25)
        for i, v in enumerate(self.list_outputs_entries):
            v.grid(row=i, column=1, sticky="w", padx=5, pady=1)
            v.config(width=10)
        for i, v in enumerate(self.list_outputs_units):
            v.grid(row=i, column=2, sticky="w", padx=5, pady=1)
            v.config(width=5)

        # Set default value
        # -----------------
        self.entry_Q1.delete(0, tk.END)
        self.entry_Q1.insert(tk.END, '168.00')

        self.entry_Q2.delete(0, tk.END)
        self.entry_Q2.insert(tk.END, '12.60')

        # Output and calculate button
        # ===========================

        self.entry_Q2r.config(stat="readonly")
        self.entry_Q2r.delete(0, tk.END)
        self.entry_Sr.config(stat="readonly")
        self.entry_Sr.delete(0, tk.END)
        self.entry_UAr.config(stat="readonly")
        self.entry_UAr.delete(0, tk.END)

        self.button_calculate = ttk.Button(
            self, text="Calculate", command=self.calculate_resultant_heat_flux
        )
        self.button_calculate.grid(
            row=12, column=5, columnspan=2, sticky="we", padx=(0, 5), pady=5
        )

    def calculate_resultant_heat_flux(self, _=None):
        """
        Yan FU, 23 Nov 2019
        Calculates and outputs the resultant heat flux at the exposed surface based on user defined inputs from the GUI.
        :param _: Placeholder, no use. No idea why tk.Tk.root.binder would forcefully feed a parameter to the func.
        :return: No.
        """

        def get_float_from_entry(list_entries_: typing.List[ttk.Entry]):
            list_entry_v = list()
            for i in list_entries_:
                try:
                    list_entry_v.append(float(str(i.get()).strip()))
                except:
                    list_entry_v.append(None)
            return list_entry_v

        list_entry = [
            self.entry_W,
            self.entry_H,
            self.entry_Q1,
            self.entry_m,
            self.entry_n,
            self.entry_Q2,
            self.entry_S,
            self.entry_UA,
        ]
        list_entry_v = get_float_from_entry(list_entry)
        W, H, Q1, m, n, Q2, S, UA = tuple(list_entry_v)

        # correction for centered receiver
        if self.checkbutton_centered_v.get() == 1:
            m = 0.5 * W
            n = 0.5 * H

        # correction for separation, to surface or boundary
        if self.checkbutton_to_boundary_v.get() == 1:
            if S is not None:
                S = 2.0 * S
        # limit UA input between 0.001 and 100
        if UA is not None:
            UA = float(max([0.001, min([100., UA])]))

        # step 2, calculate separation for given UA
        if self.checkbutton_solve_separation_v.get() == 1:
            try:
                Sr = linear_solver(
                    func=phi_parallel_any_br187,
                    dict_params=dict(W_m=W, H_m=H, w_m=m, h_m=n, S_m=S),
                    x_name='S_m',
                    y_target=Q2 / (Q1*UA/100),
                    x_upper=0.01, x_lower=1000,
                    y_tol=0.0001,
                    iter_max=10000,
                    func_multiplier=-1
                )
                Sr = 0. if Sr is None else Sr
            except Exception as e:
                if hasattr(e, "message"):
                    e = e.message
                Messenger(e, 'Error')
                Sr = ''
        else:
            Sr = ''

        # step 3, calculate UA for given separation only
        if self.checkbutton_solve_UA_v.get() == 1:
            try:
                Q2r = (phi_parallel_any_br187(W_m=W, H_m=H, w_m=m, h_m=n, S_m=S) * Q1)
                UAr = min([Q2 / Q2r * 100, 100])
            except Exception as e:
                if hasattr(e, "message"):
                    e = e.message
                Messenger(e, 'Error')
                Q2r = ''
                UAr = ''
        else:
            Q2r = ''
            UAr = ''

        # Address separation to boundary or to surface
        if self.checkbutton_to_boundary_v.get() == 1:
            try:
                S = float(S) / 2
            except (ValueError, TypeError):
                S = ''
            try:
                Sr = float(Sr) / 2
            except (ValueError, TypeError):
                Sr = ''

        # Update Entries
        # --------------
        def update_entry(entry: ttk.Entry, v):
            st = entry['state']
            entry['state'] = 'normal'
            entry.delete(0, tk.END)
            if isinstance(v, int):
                v = float(v)
                entry.insert(tk.END, f"{v:.2f}")
            elif isinstance(v, float):
                entry.insert(tk.END, f"{v:.2f}")
            elif isinstance(v, str):
                entry.insert(tk.END, v)
            else:
                entry.insert(tk.END, "")
            entry['state'] = st

        update_entry(self.entry_W, W)
        update_entry(self.entry_H, H)
        update_entry(self.entry_Q1, Q1)
        update_entry(self.entry_m, m)
        update_entry(self.entry_n, n)
        update_entry(self.entry_Q2, Q2)
        update_entry(self.entry_S, S)
        update_entry(self.entry_UA, UA)
        update_entry(self.entry_Q2r, Q2r)
        update_entry(self.entry_Sr, Sr)
        update_entry(self.entry_UAr, UAr)

    def _check_center_receiver(self):
        if self.checkbutton_centered_v.get() == 1:
            self.label_n.config(state="disabled", foreground="grey")
            self.label_m.config(state="disabled", foreground="grey")
            self.label_n_unit.config(state="disabled", foreground="grey")
            self.label_m_unit.config(state="disabled", foreground="grey")
            self.entry_n.config(state="disabled", foreground="grey")
            self.entry_m.config(state="disabled", foreground="grey")
        elif self.checkbutton_centered_v.get() == 0:
            self.label_n.config(state="normal", foreground="black")
            self.label_m.config(state="normal", foreground="black")
            self.label_n_unit.config(state="normal", foreground="black")
            self.label_m_unit.config(state="normal", foreground="black")
            self.entry_n.config(state="normal", foreground="black")
            self.entry_m.config(state="normal", foreground="black")
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")

    def _check_to_boundary(self):
        if self.checkbutton_to_boundary_v.get() == 1:
            self.label_S.config(text="½S, separation to to boundary")
            self.label_Sr.config(text="Solved ½S separation")
            self.label_UA.config(text="UA, unprotected area")
        elif self.checkbutton_to_boundary_v.get() == 0:
            self.label_S.config(text="S, separation to surface")
            self.label_Sr.config(text="Solved S separation")
            self.label_UA.config(text="UA, unprotected area")
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")

    def _check_solve_separation(self):
        if self.checkbutton_solve_separation_v.get() == 1:
            self.label_UA.config(state='normal', foreground='black')
            self.entry_UA.config(state='normal', foreground='black')
            self.label_UA_unit.config(state='normal', foreground='black')
        elif self.checkbutton_solve_separation_v.get() == 0:
            self.label_UA.config(state='disabled', foreground='grey')
            self.entry_UA.config(state='normal', foreground='grey')
            self.entry_UA.delete(0, tk.END)
            self.entry_UA.config(state='disabled', foreground='grey')
            self.label_UA_unit.config(state='disabled', foreground='grey')
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")

    def _check_solve_UA(self):
        if self.checkbutton_solve_UA_v.get() == 1:
            self.label_S.config(state='normal', foreground='black')
            self.entry_S.config(state='normal', foreground='black')
            self.label_S_unit.config(state='normal', foreground='black')
        elif self.checkbutton_solve_UA_v.get() == 0:
            self.label_S.config(state='disabled', foreground='grey')
            self.entry_S.config(state='normal', foreground='grey')
            self.entry_S.delete(0, tk.END)
            self.entry_S.config(state='disabled', foreground='grey')
            self.label_S_unit.config(state='disabled', foreground='grey')


class CalculatorPerpendicularPanels(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # General App Setting
        # ===================
        self.app_name = "B4 BR187 Calculator"  # app name
        self.app_version = _ver  # app version
        self.app_description = """
        Thermal radiation calculator\nemitter and receiver pair\nin perpendicular.
        """

        self.init_ui()

        self._check_center_receiver()
        self._check_to_boundary()
        self._check_solve_separation()
        self._check_solve_UA()

    def init_ui(self):

        # GUI LAYOUT
        # ==========

        # Large logo
        # ----------
        _, fp_radiation_figure_image = tempfile.mkstemp()
        with open(fp_radiation_figure_image, "wb") as f:
            f.write(base64.b64decode(OFR_LOGO_LARGE_PNG_BASE64))

        label_logo_image = Image.open(os.path.realpath(fp_radiation_figure_image))
        label_logo_image = label_logo_image.resize(
            (100, int(100 / 2.43)), Image.ANTIALIAS
        )
        label_logo_image = ImageTk.PhotoImage(label_logo_image)
        label_lage_logo = ttk.Label(self, image=label_logo_image)
        label_lage_logo.image = label_logo_image
        label_lage_logo.grid(row=0, column=1, rowspan=4, columnspan=2, sticky="ne", padx=(0, 5), pady=(10, 0))

        # Short description
        # -----------------
        txt = '\n'.join([self.app_description.strip(), self.app_version])
        label_description = ttk.Label(self, text=txt, anchor="nw", foreground="grey")
        label_description.grid(row=0, column=0, rowspan=4, sticky="nw", padx=(10, 0), pady=(10, 0))

        # Radiation figure
        # ----------------
        _, fp_logo_image = tempfile.mkstemp()
        with open(fp_logo_image, "wb") as f:
            f.write(base64.b64decode(PERPENDICULAR_LARGE_FIGURE_PNG_BASE64))

        label_logo_image = Image.open(os.path.realpath(fp_logo_image))
        label_logo_image = label_logo_image.resize(
            (300, int(300 * 1.04689)), Image.ANTIALIAS
        )
        label_logo_image = ImageTk.PhotoImage(label_logo_image)
        self.label_lage_logo = ttk.Label(self, image=label_logo_image)
        self.label_lage_logo.image = label_logo_image
        self.label_lage_logo.grid(row=2, rowspan=16, column=0, columnspan=3, padx=10, pady=10)

        # Create Objects
        # ==============

        # Frames
        # ------

        self.labelframe_options = ttk.Labelframe(self, text="Options")
        self.labelframe_options.grid(row=0, column=3, rowspan=3, columnspan=3, sticky='we', padx=5, pady=5, ipadx=5, ipady=5)
        self.labelframe_inputs = ttk.Labelframe(self, text="Inputs")
        self.labelframe_inputs.grid(row=3, column=3, rowspan=6, columnspan=3, sticky='we', padx=5, pady=5, ipadx=5, ipady=5)
        self.labelframe_outputs = ttk.Labelframe(self, text="Outputs")
        self.labelframe_outputs.grid(row=9, column=3, rowspan=3, columnspan=3, sticky='we', padx=5, pady=5, ipadx=5, ipady=5)

        # Options
        # -------

        self.checkbutton_centered_v = tk.IntVar(value=1)  # set default, receiver to the center of emitter
        self.checkbutton_centered = ttk.Checkbutton(self.labelframe_options, text="Centered receiver", variable=self.checkbutton_centered_v, command=self._check_center_receiver)
        self.checkbutton_to_boundary_v = tk.IntVar(value=1)  # set default, separation to notional boundary
        self.checkbutton_to_boundary = ttk.Checkbutton(self.labelframe_options, text="Separation to boundary", variable=self.checkbutton_to_boundary_v, command=self._check_to_boundary)
        self.checkbutton_solve_separation_v = tk.IntVar(value=1)
        self.checkbutton_solve_separation = ttk.Checkbutton(self.labelframe_options, text="Solve separation", variable=self.checkbutton_solve_separation_v, command=self._check_solve_separation)
        self.checkbutton_solve_UA_v = tk.IntVar(value=1)
        self.checkbutton_solve_UA = ttk.Checkbutton(self.labelframe_options, text="Solve unprotected area", variable=self.checkbutton_solve_UA_v, command=self._check_solve_UA)
        self.list_options = [
            self.checkbutton_centered, self.checkbutton_to_boundary, self.checkbutton_solve_separation, self.checkbutton_solve_UA,
        ]

        # Inputs
        # ------

        self.label_W = ttk.Label(self.labelframe_inputs, text="W, emitter width")
        self.label_H = ttk.Label(self.labelframe_inputs, text="H, emitter height")
        self.label_Q1 = ttk.Label(self.labelframe_inputs, text="Q1, emitter HT (84, 168)")
        self.label_m = ttk.Label(self.labelframe_inputs, text="m, receiver loc. 1")
        self.label_n = ttk.Label(self.labelframe_inputs, text="n, receiver loc. 2")
        self.label_Q2 = ttk.Label(self.labelframe_inputs, text="Q2, receiver critical HT (12.6)")
        self.label_S = ttk.Label(self.labelframe_inputs, text="S, separation")
        self.label_UA = ttk.Label(self.labelframe_inputs, text="UA to solve separation")
        self.list_inputs_labels = [
            self.label_W, self.label_H, self.label_Q1,
            self.label_m, self.label_n, self.label_Q2,
            self.label_S, self.label_UA
        ]

        self.entry_W = ttk.Entry(self.labelframe_inputs)
        self.entry_H = ttk.Entry(self.labelframe_inputs)
        self.entry_Q1 = ttk.Entry(self.labelframe_inputs)
        self.entry_m = ttk.Entry(self.labelframe_inputs)
        self.entry_n = ttk.Entry(self.labelframe_inputs)
        self.entry_Q2 = ttk.Entry(self.labelframe_inputs)
        self.entry_S = ttk.Entry(self.labelframe_inputs)
        self.entry_UA = ttk.Entry(self.labelframe_inputs)
        self.list_inputs_entries = [
            self.entry_W, self.entry_H, self.entry_Q1,
            self.entry_m, self.entry_n, self.entry_Q2,
            self.entry_S, self.entry_UA
        ]

        self.label_W_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_H_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_Q1_unit = ttk.Label(self.labelframe_inputs, text="kW/m²")
        self.label_m_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_n_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_Q2_unit = ttk.Label(self.labelframe_inputs, text="kW/m²")
        self.label_S_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_UA_unit = ttk.Label(self.labelframe_inputs, text='%')
        self.list_inputs_units = [
            self.label_W_unit, self.label_H_unit, self.label_Q1_unit,
            self.label_m_unit, self.label_n_unit, self.label_Q2_unit,
            self.label_S_unit, self.label_UA_unit
        ]

        # Outputs
        # -------

        self.label_Q2r = ttk.Label(self.labelframe_outputs, text="Solved Q2 at receiver")
        self.label_Sr = ttk.Label(self.labelframe_outputs, text="Solved separation S")
        self.label_UAr = ttk.Label(self.labelframe_outputs, text="Solved UA")
        self.list_outputs_labels = [
            self.label_Q2r, self.label_Sr, self.label_UAr
        ]
        self.entry_Q2r = ttk.Entry(self.labelframe_outputs)
        self.entry_Sr = ttk.Entry(self.labelframe_outputs)
        self.entry_UAr = ttk.Entry(self.labelframe_outputs)
        self.list_outputs_entries = [
            self.entry_Q2r, self.entry_Sr, self.entry_UAr
        ]
        self.label_Q2r_unit = ttk.Label(self.labelframe_outputs, text="kW/m²")
        self.label_Sr_unit = ttk.Label(self.labelframe_outputs, text="m")
        self.label_UAr_unit = ttk.Label(self.labelframe_outputs, text="%")
        self.list_outputs_units = [
            self.label_Q2r_unit, self.label_Sr_unit, self.label_UAr_unit
        ]

        # Set Grid Location
        # -----------------

        for i, v in enumerate(self.list_options):
            v.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            # v.config(width=25)

        for i, v in enumerate(self.list_inputs_labels):
            v.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            v.config(width=25)
        for i, v in enumerate(self.list_inputs_entries):
            v.grid(row=i, column=1, sticky="w", padx=5, pady=1)
            v.config(width=10)
        for i, v in enumerate(self.list_inputs_units):
            v.grid(row=i, column=2, sticky="w", padx=5, pady=1)
            v.config(width=5)

        for i, v in enumerate(self.list_outputs_labels):
            v.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            v.config(width=25)
        for i, v in enumerate(self.list_outputs_entries):
            v.grid(row=i, column=1, sticky="w", padx=5, pady=1)
            v.config(width=10)
        for i, v in enumerate(self.list_outputs_units):
            v.grid(row=i, column=2, sticky="w", padx=5, pady=1)
            v.config(width=5)

        # Set default value
        # -----------------

        self.entry_Q1.delete(0, tk.END)
        self.entry_Q1.insert(tk.END, '168.00')

        self.entry_Q2.delete(0, tk.END)
        self.entry_Q2.insert(tk.END, '12.60')

        # Output and calculate button
        # ===========================

        self.entry_Q2r.config(stat="readonly")
        self.entry_Q2r.delete(0, tk.END)
        self.entry_Sr.config(stat="readonly")
        self.entry_Sr.delete(0, tk.END)
        self.entry_UAr.config(stat="readonly")
        self.entry_UAr.delete(0, tk.END)

        self.button_calculate = ttk.Button(
            self, text="Calculate", command=self.calculate_resultant_heat_flux
        )
        self.button_calculate.grid(
            row=12, column=5, columnspan=2, sticky="we", padx=(0, 5), pady=5
        )

    def calculate_resultant_heat_flux(self, _=None):
        """
        Yan FU, 23 Nov 2019
        Calculates and outputs the resultant heat flux at the exposed surface based on user defined inputs from the GUI.
        :param _: Placeholder, no use. No idea why tk.Tk.root.binder would forcefully feed a parameter to the func.
        :return: No.
        """

        def get_float_from_entry(list_entries_: typing.List[ttk.Entry]):
            list_entry_v = list()
            for i in list_entries_:
                try:
                    list_entry_v.append(float(str(i.get()).strip()))
                except:
                    list_entry_v.append(None)
            return list_entry_v

        list_entry = [
            self.entry_W,
            self.entry_H,
            self.entry_Q1,
            self.entry_m,
            self.entry_n,
            self.entry_Q2,
            self.entry_S,
            self.entry_UA,
        ]
        list_entry_v = get_float_from_entry(list_entry)
        W, H, Q1, m, n, Q2, S, UA = tuple(list_entry_v)

        # correction for centered receiver
        if self.checkbutton_centered_v.get() == 1:
            n = 0.5 * H

        # correction for separation, to surface or boundary
        if self.checkbutton_to_boundary_v.get() == 1:
            if S is not None:
                S = 2.0 * S
        # limit UA input between 0.001 and 100
        if UA is not None:
            UA = float(max([0.001, min([100., UA])]))

        # step 2, calculate separation for given UA
        if self.checkbutton_solve_separation_v.get() == 1:
            try:
                Sr = linear_solver(
                    func=phi_perpendicular_any_br187,
                    dict_params=dict(W_m=W, H_m=H, w_m=m, h_m=n, S_m=S),
                    x_name='S_m',
                    y_target=Q2 / (Q1*UA/100),
                    x_upper=0.01, x_lower=1000,
                    y_tol=0.0001,
                    iter_max=10000,
                    func_multiplier=-1
                )
                Sr = 0. if Sr is None else Sr
            except Exception as e:
                if hasattr(e, "message"):
                    e = e.message
                Messenger(e, 'Error')
                Sr = ''
        else:
            Sr = ''

        # step 3, calculate UA for given separation only
        if self.checkbutton_solve_UA_v.get() == 1:
            try:
                Q2r = (phi_parallel_any_br187(W_m=W, H_m=H, w_m=m, h_m=n, S_m=S) * Q1)
                UAr = min([Q2 / Q2r * 100, 100])
            except Exception as e:
                if hasattr(e, "message"):
                    e = e.message
                Messenger(e, 'Error')
                Q2r = ''
                UAr = ''
        else:
            Q2r = ''
            UAr = ''

        # Address separation to boundary or to surface
        if self.checkbutton_to_boundary_v.get() == 1:
            try:
                S = float(S) / 2
            except (ValueError, TypeError):
                S = ''
            try:
                Sr = float(Sr) / 2
            except (ValueError, TypeError):
                Sr = ''

        # Update Entries
        # --------------
        def update_entry(entry: ttk.Entry, v):
            st = entry['state']
            entry['state'] = 'normal'
            entry.delete(0, tk.END)
            if isinstance(v, int):
                v = float(v)
                entry.insert(tk.END, f"{v:.2f}")
            elif isinstance(v, float):
                entry.insert(tk.END, f"{v:.2f}")
            elif isinstance(v, str):
                entry.insert(tk.END, v)
            else:
                entry.insert(tk.END, "")
            entry['state'] = st

        update_entry(self.entry_W, W)
        update_entry(self.entry_H, H)
        update_entry(self.entry_Q1, Q1)
        update_entry(self.entry_m, m)
        update_entry(self.entry_n, n)
        update_entry(self.entry_Q2, Q2)
        update_entry(self.entry_S, S)
        update_entry(self.entry_UA, UA)
        update_entry(self.entry_Q2r, Q2r)
        update_entry(self.entry_Sr, Sr)
        update_entry(self.entry_UAr, UAr)

    def _check_center_receiver(self):
        if self.checkbutton_centered_v.get() == 1:
            self.label_n.config(state="disabled", foreground="grey")
            self.label_n_unit.config(state="disabled", foreground="grey")
            self.entry_n.config(state="disabled", foreground="grey")
        elif self.checkbutton_centered_v.get() == 0:
            self.label_n.config(state="normal", foreground="black")
            self.label_n_unit.config(state="normal", foreground="black")
            self.entry_n.config(state="normal", foreground="black")
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")

    def _check_to_boundary(self):
        if self.checkbutton_to_boundary_v.get() == 1:
            self.label_S.config(text="½S, separation to solve UA")
            self.label_Sr.config(text="Solved ½S separation")
            self.label_UA.config(text="UA, to solve ½S")
        elif self.checkbutton_to_boundary_v.get() == 0:
            self.label_S.config(text="S, separation to solve UA")
            self.label_Sr.config(text="Solved S separation")
            self.label_UA.config(text="UA, to solve S")
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")

    def _check_solve_separation(self):
        if self.checkbutton_solve_separation_v.get() == 1:
            self.label_UA.config(state='normal', foreground='black')
            self.entry_UA.config(state='normal', foreground='black')
            self.label_UA_unit.config(state='normal', foreground='black')
        elif self.checkbutton_solve_separation_v.get() == 0:
            self.label_UA.config(state='disabled', foreground='grey')
            self.entry_UA.config(state='normal', foreground='grey')
            self.entry_UA.delete(0, tk.END)
            self.entry_UA.config(state='disabled', foreground='grey')
            self.label_UA_unit.config(state='disabled', foreground='grey')
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")

    def _check_solve_UA(self):
        if self.checkbutton_solve_UA_v.get() == 1:
            self.label_S.config(state='normal', foreground='black')
            self.entry_S.config(state='normal', foreground='black')
            self.label_S_unit.config(state='normal', foreground='black')
        elif self.checkbutton_solve_UA_v.get() == 0:
            self.label_S.config(state='disabled', foreground='grey')
            self.entry_S.config(state='normal', foreground='grey')
            self.entry_S.delete(0, tk.END)
            self.entry_S.config(state='disabled', foreground='grey')
            self.label_S_unit.config(state='disabled', foreground='grey')


def main():
    my_gui = Calculator()
    my_gui.mainloop()


if __name__ == "__main__":
    main()
