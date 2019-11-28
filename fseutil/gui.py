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
        Thermal radiation calculator\nemitter and receiver pair\nin perpendicular.
        """

        self.init_ui()

        self.check_center_receiver()
        self.check_to_boundary()

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
        label_lage_logo.grid(row=0, column=1, columnspan=2, sticky="se", padx=(0, 5), pady=(0, 0))

        # Short description
        # -----------------
        txt = '\n'.join([self.app_description.strip(), self.app_version])
        label_description = ttk.Label(self, text=txt, anchor="nw", foreground="grey")
        label_description.grid(row=0, column=0, rowspan=2, sticky="ws", padx=(10, 0), pady=(10, 0))

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
        self.label_lage_logo.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Create Objects
        # ==============

        # Frames
        # ------

        self.labelframe_options = ttk.Labelframe(self, text="Options")
        self.labelframe_options.grid(row=3, column=0, rowspan=1, columnspan=3, sticky='we', padx=5, pady=5, ipadx=5, ipady=5)
        self.labelframe_inputs = ttk.Labelframe(self, text="Inputs")
        self.labelframe_inputs.grid(row=7, column=0, rowspan=6, columnspan=3, sticky='we', padx=5, pady=5, ipadx=5, ipady=5)
        self.labelframe_outputs = ttk.Labelframe(self, text="Outputs")
        self.labelframe_outputs.grid(row=13, column=0, rowspan=3, columnspan=3, sticky='we', padx=5, pady=5, ipadx=5, ipady=5)

        # Options
        # -------

        self.checkbutton_centered_v = tk.IntVar(value=1)  # set default, receiver to the center of emitter
        self.checkbutton_centered = ttk.Checkbutton(self.labelframe_options, text="Centered receiver", variable=self.checkbutton_centered_v, command=self.check_center_receiver)
        self.checkbutton_to_boundary_v = tk.IntVar(value=1)  # set default, separation to notional boundary
        self.checkbutton_to_boundary = ttk.Checkbutton(self.labelframe_options, text="Separation to boundary", variable=self.checkbutton_to_boundary_v, command=self.check_to_boundary)
        self.list_options = [
            self.checkbutton_centered, self.checkbutton_to_boundary
        ]

        # Inputs
        # ------

        self.label_W = ttk.Label(self.labelframe_inputs, text="W, emitter width")
        self.label_H = ttk.Label(self.labelframe_inputs, text="H, emitter height")
        self.label_Q1 = ttk.Label(self.labelframe_inputs, text="Q1, emitter HT (84, 168)")
        self.label_m = ttk.Label(self.labelframe_inputs, text="m, receiver loc. 1")
        self.label_n = ttk.Label(self.labelframe_inputs, text="n, receiver loc. 2")
        self.label_Q2 = ttk.Label(self.labelframe_inputs, text="Q2, receiver HT (12.6)")
        self.label_S = ttk.Label(self.labelframe_inputs, text="S, separation")
        self.list_inputs_labels = [
            self.label_W, self.label_H, self.label_Q1, self.label_m, self.label_n, self.label_Q2, self.label_S
        ]

        self.entry_W = ttk.Entry(self.labelframe_inputs)
        self.entry_H = ttk.Entry(self.labelframe_inputs)
        self.entry_Q1 = ttk.Entry(self.labelframe_inputs)
        self.entry_m = ttk.Entry(self.labelframe_inputs)
        self.entry_n = ttk.Entry(self.labelframe_inputs)
        self.entry_Q2 = ttk.Entry(self.labelframe_inputs)
        self.entry_S = ttk.Entry(self.labelframe_inputs)
        self.list_inputs_entries = [
            self.entry_W, self.entry_H, self.entry_Q1, self.entry_m, self.entry_n, self.entry_Q2, self.entry_S
        ]

        self.label_W_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_H_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_Q1_unit = ttk.Label(self.labelframe_inputs, text="kW/m²")
        self.label_m_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_n_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_Q2_unit = ttk.Label(self.labelframe_inputs, text="kW/m²")
        self.label_S_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.list_inputs_units = [
            self.label_W_unit, self.label_H_unit, self.label_Q1_unit,
            self.label_m_unit, self.label_n_unit, self.label_Q2_unit,
            self.label_S_unit
        ]

        # Outputs
        # -------

        self.label_Q2r = ttk.Label(self.labelframe_outputs, text="Calculated HT at receiver")
        self.label_Sr = ttk.Label(self.labelframe_outputs, text="Calculated separation S")
        self.label_upa = ttk.Label(self.labelframe_outputs, text="Calculated UPA")
        self.list_outputs_labels = [
            self.label_Q2r, self.label_Sr, self.label_upa
        ]
        self.entry_Q2r = ttk.Entry(self.labelframe_outputs)
        self.entry_Sr = ttk.Entry(self.labelframe_outputs)
        self.entry_upa = ttk.Entry(self.labelframe_outputs)
        self.list_outputs_entries = [
            self.entry_Q2r, self.entry_Sr, self.entry_upa
        ]
        self.label_Q2r_unit = ttk.Label(self.labelframe_outputs, text="kW/m²")
        self.label_Sr_unit = ttk.Label(self.labelframe_outputs, text="m")
        self.label_upa_unit = ttk.Label(self.labelframe_outputs, text="%")
        self.list_outputs_units = [
            self.label_Q2r_unit, self.label_Sr_unit, self.label_upa_unit
        ]

        # Set Grid Location
        # -----------------

        self.checkbutton_centered.grid(row=0, column=0, sticky="w", padx=5, pady=1)
        self.checkbutton_to_boundary.grid(row=1, column=0, sticky="w", padx=5, pady=1)

        for i, v in enumerate(self.list_inputs_labels):
            v.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            v.config(width=22)
        for i, v in enumerate(self.list_inputs_entries):
            v.grid(row=i, column=1, sticky="w", padx=5, pady=1)
            v.config(width=10)
        for i, v in enumerate(self.list_inputs_units):
            v.grid(row=i, column=2, sticky="w", padx=5, pady=1)
            v.config(width=5)
        for i, v in enumerate(self.list_outputs_labels):
            v.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            v.config(width=22)
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
        self.entry_upa.config(stat="readonly")
        self.entry_upa.delete(0, tk.END)

        self.button_calculate = ttk.Button(
            self, text="Calculate", command=self.calculate_resultant_heat_flux
        )
        self.button_calculate.grid(
            row=16, column=1, columnspan=2, sticky="we", padx=(0, 10), pady=10
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

        list_label = [
            self.label_W,
            self.label_H,
            self.label_Q1,
            self.label_m,
            self.label_n,
            self.label_Q2,
            self.label_S
        ]
        list_entry = [
            self.entry_W,
            self.entry_H,
            self.entry_Q1,
            self.entry_m,
            self.entry_n,
            self.entry_Q2,
            self.entry_S
        ]
        list_entry_v = get_float_from_entry(list_entry)

        print("BEFORE CALCULATION")
        print(
            "\n".join(
                "{:40.40} {}".format(v.cget("text") + ":", list_entry_v[i])
                for i, v in enumerate(list_label)
            )
        )

        W, H, Q1, m, n, Q2, S = tuple(list_entry_v)

        # calculate heat flux at receiver, Q2
        try:
            m = 0.5 * W if self.checkbutton_centered_v.get() == 1 else m
            n = 0.5 * H if self.checkbutton_centered_v.get() == 1 else n
            S = 2.0 * S if self.checkbutton_to_boundary_v.get() == 1 else S
            Q2_calculated = (phi_parallel_any_br187(W_m=W, H_m=H, w_m=m, h_m=n, S_m=S) * Q1)

            Sr = linear_solver(
                func=phi_parallel_any_br187,
                dict_params=dict(W_m=W, H_m=H, w_m=m, h_m=n, S_m=S),
                x_name='S_m',
                y_target=Q2 / Q1,
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
            return 0

        if Q2 is None:
            # if Q2 not provided, output calculated Q2 only
            upa = ""
            Q2r = Q2_calculated
        else:
            # if Q2 is provided, output both calculated Q2 and upa
            upa = min([Q2 / Q2_calculated * 100, 100])
            Q2r = Q2_calculated

        try:
            print("AFTER CALCULATION")
            print(
                "\n".join(
                    "{:40.40} {}".format(v.cget("text") + ":", list_entry_v[i])
                    for i, v in enumerate(list_label)
                )
            )
        except Exception:
            pass

        # Update Entries
        # --------------
        # store Entry state, to restore later
        list_tk = [
            self.entry_W,
            self.entry_H,
            self.entry_Q1,
            self.entry_m,
            self.entry_n,
            self.entry_Q2,
            self.entry_S,
            self.entry_Q2r,
            self.entry_Sr,
            self.entry_upa,
        ]
        list_tk_states = [i["state"] for i in list_tk]

        # set Entry state to 'normal' to able to write value
        for i in list_tk:
            i["state"] = "normal"
            i.delete(0, tk.END)

        # delete existing Entry value
        for i in list_tk:
            i.delete(0, tk.END)

        # set Entry value to new values
        S = S / 2 if self.checkbutton_to_boundary_v.get() == 1 else S
        Sr = Sr / 2 if self.checkbutton_to_boundary_v.get() == 1 else Sr
        self.entry_W.insert(tk.END, f"{W:.2f}")
        self.entry_H.insert(tk.END, f"{H:.2f}")
        self.entry_Q1.insert(tk.END, f'{Q1:.2f}')
        self.entry_m.insert(tk.END, f"{m:.2f}")
        self.entry_n.insert(tk.END, f"{n:.2f}")
        self.entry_Q2.insert(tk.END, f"{Q2:.2f}")
        self.entry_S.insert(tk.END, f"{S:.2f}")
        self.entry_Q2r.insert(tk.END, f"{Q2r:.2f}")
        self.entry_Sr.insert(tk.END, f"{Sr:.2f}")
        if isinstance(upa, str):
            self.entry_upa.insert(tk.END, "")
        else:
            self.entry_upa.insert(tk.END, f"{upa:.2f}")

        # restore Entry state
        for i, v in enumerate(list_tk):
            v["state"] = list_tk_states[i]

    def check_center_receiver(self):
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

    def check_to_boundary(self):
        if self.checkbutton_to_boundary_v.get() == 1:
            self.label_S.config(text="½S, separation to boundary")
            self.label_Sr.config(text="Calculated separation ½S")
        elif self.checkbutton_to_boundary_v.get() == 0:
            self.label_S.config(text="S, separation to surface")
            self.label_Sr.config(text="Calculated separation S")
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")


class CalculatorPerpendicularPanels(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # General App Setting
        # ===================
        self.app_name = "B4 BR187 Calculator"  # app name
        self.app_version = _ver  # app version
        self.app_description = """
        Thermal radiation calculator\nemitter and receiver pair\nin parallel.
        """

        self.init_ui()

        self.check_center_receiver()
        self.check_to_boundary()

        # self.master.resizable(0, 0)
        # set short cut, calculate when enter is pressed
        # self.root = None
        # if root:
        #     root.bind(sequence="<Return>", func=self.calculate_resultant_heat_flux)

    def init_ui(self):

        # GUI LAYOUT
        # ==========

        # Large logo
        # ----------
        _, fp_logo = tempfile.mkstemp()
        with open(fp_logo, "wb") as f:
            f.write(base64.b64decode(OFR_LOGO_LARGE_PNG_BASE64))

        label_logo_image = Image.open(os.path.realpath(fp_logo))
        label_logo_image = label_logo_image.resize(
            (100, int(100 / 2.43)), Image.ANTIALIAS
        )
        label_logo_image = ImageTk.PhotoImage(label_logo_image)
        label_lage_logo = ttk.Label(self, image=label_logo_image)
        label_lage_logo.image = label_logo_image
        label_lage_logo.grid(row=0, column=1, columnspan=2, sticky="se", padx=(0, 5), pady=(0, 0))

        # Short description
        # -----------------
        txt = '\n'.join([self.app_description.strip(), self.app_version])
        label_description = ttk.Label(self, text=txt, anchor="nw", foreground="grey")
        label_description.grid(row=0, column=0, rowspan=2, sticky="ws", padx=(10, 0), pady=(10, 0))

        # Radiation figure
        # ----------------
        _, fp_main_figure = tempfile.mkstemp()
        with open(fp_main_figure, "wb") as f:
            f.write(base64.b64decode(PERPENDICULAR_LARGE_FIGURE_PNG_BASE64))
        main_figure_image = Image.open(os.path.realpath(fp_main_figure))
        main_figure_image = main_figure_image.resize(
            (300, int(300 * 1.04689)), Image.ANTIALIAS
        )
        main_figure_image = ImageTk.PhotoImage(main_figure_image)
        label_main_figure = ttk.Label(self, image=main_figure_image)
        label_main_figure.image = main_figure_image
        label_main_figure.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Create Objects
        # ==============

        # Frames
        # ------

        self.labelframe_options = ttk.Labelframe(self, text="Options")
        self.labelframe_options.grid(row=3, column=0, rowspan=1, columnspan=3, sticky='we', padx=5, pady=5, ipadx=5, ipady=5)
        self.labelframe_inputs = ttk.Labelframe(self, text="Inputs")
        self.labelframe_inputs.grid(row=7, column=0, rowspan=6, columnspan=3, sticky='we', padx=5, pady=5, ipadx=5, ipady=5)
        self.labelframe_outputs = ttk.Labelframe(self, text="Outputs")
        self.labelframe_outputs.grid(row=13, column=0, rowspan=3, columnspan=3, sticky='we', padx=5, pady=5, ipadx=5, ipady=5)

        # Options
        # -------

        self.checkbutton_centered_v = tk.IntVar(value=1)  # set default, receiver to the center of emitter
        self.checkbutton_centered = ttk.Checkbutton(self.labelframe_options, text="Centered receiver", variable=self.checkbutton_centered_v, command=self.check_center_receiver)
        self.checkbutton_to_boundary_v = tk.IntVar(value=1)  # set default, separation to notional boundary
        self.checkbutton_to_boundary = ttk.Checkbutton(self.labelframe_options, text="Separation to boundary", variable=self.checkbutton_to_boundary_v, command=self.check_to_boundary)
        self.list_options = [
            self.checkbutton_centered, self.checkbutton_to_boundary
        ]

        # Inputs
        # ------

        self.label_W = ttk.Label(self.labelframe_inputs, text="W, emitter width")
        self.label_H = ttk.Label(self.labelframe_inputs, text="H, emitter height")
        self.label_Q1 = ttk.Label(self.labelframe_inputs, text="Q1, emitter HT (84, 168)")
        self.label_m = ttk.Label(self.labelframe_inputs, text="m, receiver loc. 1")
        self.label_n = ttk.Label(self.labelframe_inputs, text="n, receiver loc. 2")
        self.label_Q2 = ttk.Label(self.labelframe_inputs, text="Q2, receiver HT (12.6)")
        self.label_S = ttk.Label(self.labelframe_inputs, text="S, separation")
        self.list_inputs_labels = [
            self.label_W, self.label_H, self.label_Q1, self.label_m, self.label_n, self.label_Q2, self.label_S
        ]

        self.entry_W = ttk.Entry(self.labelframe_inputs)
        self.entry_H = ttk.Entry(self.labelframe_inputs)
        self.entry_Q1 = ttk.Entry(self.labelframe_inputs)
        self.entry_m = ttk.Entry(self.labelframe_inputs)
        self.entry_n = ttk.Entry(self.labelframe_inputs)
        self.entry_Q2 = ttk.Entry(self.labelframe_inputs)
        self.entry_S = ttk.Entry(self.labelframe_inputs)
        self.list_inputs_entries = [
            self.entry_W, self.entry_H, self.entry_Q1, self.entry_m, self.entry_n, self.entry_Q2, self.entry_S
        ]

        self.label_W_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_H_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_Q1_unit = ttk.Label(self.labelframe_inputs, text="kW/m²")
        self.label_m_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_n_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.label_Q2_unit = ttk.Label(self.labelframe_inputs, text="kW/m²")
        self.label_S_unit = ttk.Label(self.labelframe_inputs, text="m")
        self.list_inputs_units = [
            self.label_W_unit, self.label_H_unit, self.label_Q1_unit,
            self.label_m_unit, self.label_n_unit, self.label_Q2_unit,
            self.label_S_unit
        ]

        # Outputs
        # -------

        self.label_Q2r = ttk.Label(self.labelframe_outputs, text="Calculated HT at receiver")
        self.label_Sr = ttk.Label(self.labelframe_outputs, text="Calculated separation S")
        self.label_upa = ttk.Label(self.labelframe_outputs, text="Calculated UPA")
        self.list_outputs_labels = [
            self.label_Q2r, self.label_Sr, self.label_upa
        ]
        self.entry_Q2r = ttk.Entry(self.labelframe_outputs)
        self.entry_Sr = ttk.Entry(self.labelframe_outputs)
        self.entry_upa = ttk.Entry(self.labelframe_outputs)
        self.list_outputs_entries = [
            self.entry_Q2r, self.entry_Sr, self.entry_upa
        ]
        self.label_Q2r_unit = ttk.Label(self.labelframe_outputs, text="kW/m²")
        self.label_Sr_unit = ttk.Label(self.labelframe_outputs, text="m")
        self.label_upa_unit = ttk.Label(self.labelframe_outputs, text="%")
        self.list_outputs_units = [
            self.label_Q2r_unit, self.label_Sr_unit, self.label_upa_unit
        ]

        # Set Grid Location
        # -----------------

        self.checkbutton_centered.grid(row=0, column=0, sticky="w", padx=5, pady=1)
        self.checkbutton_to_boundary.grid(row=1, column=0, sticky="w", padx=5, pady=1)

        for i, v in enumerate(self.list_inputs_labels):
            v.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            v.config(width=22)
        for i, v in enumerate(self.list_inputs_entries):
            v.grid(row=i, column=1, sticky="w", padx=5, pady=1)
            v.config(width=10)
        for i, v in enumerate(self.list_inputs_units):
            v.grid(row=i, column=2, sticky="w", padx=5, pady=1)
            v.config(width=5)
        for i, v in enumerate(self.list_outputs_labels):
            v.grid(row=i, column=0, sticky="w", padx=5, pady=1)
            v.config(width=22)
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
        self.entry_upa.config(stat="readonly")
        self.entry_upa.delete(0, tk.END)

        self.button_calculate = ttk.Button(
            self, text="Calculate", command=self.calculate_resultant_heat_flux
        )
        self.button_calculate.grid(
            row=16, column=1, columnspan=2, sticky="we", padx=(0, 10), pady=10
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

        list_label = [
            self.label_W,
            self.label_H,
            self.label_Q1,
            self.label_m,
            self.label_n,
            self.label_Q2,
            self.label_S
        ]
        list_entry = [
            self.entry_W,
            self.entry_H,
            self.entry_Q1,
            self.entry_m,
            self.entry_n,
            self.entry_Q2,
            self.entry_S
        ]
        list_entry_v = get_float_from_entry(list_entry)

        print("BEFORE CALCULATION")
        print(
            "\n".join(
                "{:40.40} {}".format(v.cget("text") + ":", list_entry_v[i])
                for i, v in enumerate(list_label)
            )
        )

        W, H, Q1, m, n, Q2, S = tuple(list_entry_v)

        # calculate heat flux at receiver, Q2
        try:
            m = 0.5 * W if self.checkbutton_centered_v.get() == 1 else m
            n = 0.5 * H if self.checkbutton_centered_v.get() == 1 else n
            S = 2.0 * S if self.checkbutton_to_boundary_v.get() == 1 else S
            Q2_calculated = (phi_perpendicular_any_br187(W_m=W, H_m=H, w_m=m, h_m=n, S_m=S) * Q1)

            Sr = linear_solver(
                func=phi_perpendicular_any_br187,
                dict_params=dict(W_m=W, H_m=H, w_m=m, h_m=n, S_m=S),
                x_name='S_m',
                y_target=Q2 / Q1,
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
            return 0

        if Q2 is None:
            # if Q2 not provided, output calculated Q2 only
            upa = ""
            Q2r = Q2_calculated
        else:
            # if Q2 is provided, output both calculated Q2 and upa
            upa = min([Q2 / Q2_calculated * 100, 100])
            Q2r = Q2_calculated

        try:
            print("AFTER CALCULATION")
            print(
                "\n".join(
                    "{:40.40} {}".format(v.cget("text") + ":", list_entry_v[i])
                    for i, v in enumerate(list_label)
                )
            )
        except Exception:
            pass

        # Update Entries
        # --------------
        # store Entry state, to restore later
        list_tk = [
            self.entry_W,
            self.entry_H,
            self.entry_Q1,
            self.entry_m,
            self.entry_n,
            self.entry_Q2,
            self.entry_S,
            self.entry_Q2r,
            self.entry_Sr,
            self.entry_upa,
        ]
        list_tk_states = [i["state"] for i in list_tk]

        # set Entry state to 'normal' to able to write value
        for i in list_tk:
            i["state"] = "normal"
            i.delete(0, tk.END)

        # delete existing Entry value
        for i in list_tk:
            i.delete(0, tk.END)

        # set Entry value to new values
        S = S / 2 if self.checkbutton_to_boundary_v.get() == 1 else S
        Sr = Sr / 2 if self.checkbutton_to_boundary_v.get() == 1 else Sr
        self.entry_W.insert(tk.END, f"{W:.2f}")
        self.entry_H.insert(tk.END, f"{H:.2f}")
        self.entry_Q1.insert(tk.END, f'{Q1:.2f}')
        self.entry_m.insert(tk.END, f"{m:.2f}")
        self.entry_n.insert(tk.END, f"{n:.2f}")
        self.entry_Q2.insert(tk.END, f"{Q2:.2f}")
        self.entry_S.insert(tk.END, f"{S:.2f}")
        self.entry_Q2r.insert(tk.END, f"{Q2r:.2f}")
        self.entry_Sr.insert(tk.END, f"{Sr:.2f}")
        if isinstance(upa, str):
            self.entry_upa.insert(tk.END, "")
        else:
            self.entry_upa.insert(tk.END, f"{upa:.2f}")

        # restore Entry state
        for i, v in enumerate(list_tk):
            v["state"] = list_tk_states[i]

    def check_center_receiver(self):
        if self.checkbutton_centered_v.get() == 1:
            self.label_n.config(state="disabled", foreground="grey")
            # self.label_m.config(state="disabled", foreground="grey")
            self.label_n_unit.config(state="disabled", foreground="grey")
            # self.label_m_unit.config(state="disabled", foreground="grey")
            self.entry_n.config(state="disabled", foreground="grey")
            # self.entry_m.config(state="disabled", foreground="grey")
        elif self.checkbutton_centered_v.get() == 0:
            self.label_n.config(state="normal", foreground="black")
            # self.label_m.config(state="normal", foreground="black")
            self.label_n_unit.config(state="normal", foreground="black")
            # self.label_m_unit.config(state="normal", foreground="black")
            self.entry_n.config(state="normal", foreground="black")
            # self.entry_m.config(state="normal", foreground="black")
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")

    def check_to_boundary(self):
        if self.checkbutton_to_boundary_v.get() == 1:
            self.label_S.config(text="½S, separation to boundary")
            self.label_Sr.config(text="Calculated separation ½S")
        elif self.checkbutton_to_boundary_v.get() == 0:
            self.label_S.config(text="S, separation to surface")
            self.label_Sr.config(text="Calculated separation S")
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")


def main():
    my_gui = Calculator()
    my_gui.mainloop()


if __name__ == "__main__":
    main()
