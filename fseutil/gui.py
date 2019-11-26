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

        self.notebook.add(CalculatorParallelPanels(self.notebook), text='Parallel Panels', compound=tk.TOP)
        self.notebook.add(CalculatorPerpendicularlPanels(self.notebook), text='Perpendicular Panels', compound=tk.TOP)


class CalculatorParallelPanels(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # General App Setting
        # ===================
        self.app_name = "B4 BR187 Calculator"  # app name
        self.app_version = _ver  # app version
        self.app_description = """
        Thermal radiation calculator for\nparallel and perpendicular faced\nemitter and receiver pair.
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
        _, fp_radiation_figure_image = tempfile.mkstemp()
        with open(fp_radiation_figure_image, "wb") as f:
            f.write(base64.b64decode(OFR_LOGO_LARGE_PNG_BASE64))

        label_logo_image = Image.open(os.path.realpath(fp_radiation_figure_image))
        label_logo_image = label_logo_image.resize(
            (150, int(150 / 2.43)), Image.ANTIALIAS
        )
        label_logo_image = ImageTk.PhotoImage(label_logo_image)
        self.label_lage_logo = ttk.Label(self, image=label_logo_image)
        self.label_lage_logo.image = label_logo_image
        self.label_lage_logo.grid(row=0, column=1, columnspan=2, sticky="ne", padx=10, pady=10)

        # Short description
        # -----------------
        description_str = '\n'.join([self.app_name, self.app_version, '', self.app_description.strip()])
        self.label_short_description = ttk.Label(
            self, text=description_str, anchor="e", foreground="grey"
        )
        self.label_short_description.grid(
            row=0, column=0, sticky="w", padx=10, pady=10
        )

        # Radiation figure
        # ----------------
        _, fp_logo_image = tempfile.mkstemp()
        with open(fp_logo_image, "wb") as f:
            f.write(base64.b64decode(PARALLEL_LARGE_FIGURE_PNG_BASE64))

        label_logo_image = Image.open(os.path.realpath(fp_logo_image))
        label_logo_image = label_logo_image.resize(
            (400, int(400 / 1.010)), Image.ANTIALIAS
        )
        label_logo_image = ImageTk.PhotoImage(label_logo_image)
        self.label_lage_logo = ttk.Label(self, image=label_logo_image)
        self.label_lage_logo.image = label_logo_image
        self.label_lage_logo.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Input
        # =====

        # Create Objects
        # --------------

        self.checkbutton_centered_v = tk.IntVar(value=1)  # set default, receiver to the center of emitter
        self.checkbutton_centered = ttk.Checkbutton(self, text="Centered receiver", variable=self.checkbutton_centered_v, command=self.check_center_receiver)
        self.checkbutton_to_boundary_v = tk.IntVar(value=1)  # set default, separation to notional boundary
        self.checkbutton_to_boundary = ttk.Checkbutton(self, text="Separation to boundary", variable=self.checkbutton_to_boundary_v, command=self.check_to_boundary, )

        self.label_W = ttk.Label(self, text="W, emitter width")
        self.label_H = ttk.Label(self, text="H, emitter height")
        self.label_m = ttk.Label(self, text="m, receiver width")
        self.label_n = ttk.Label(self, text="n, receiver height")
        self.label_Q1 = ttk.Label(self, text="Q1, emitter HT (84, 168)")
        self.label_Q2 = ttk.Label(self, text="Q2, permitted HT (optional, 12.6)")
        self.label_S = ttk.Label(self, text="S, separation")
        self.label_upa = ttk.Label(self, text="Calculated Permitted UPA")

        self.entry_W = ttk.Entry(self)
        self.entry_H = ttk.Entry(self)
        self.entry_m = ttk.Entry(self)
        self.entry_n = ttk.Entry(self)
        self.entry_Q1 = ttk.Entry(self)
        # self.option_Q1_v = tk.StringVar(self.master)
        # self.option_Q1_v.set("168.00")
        # self.option_Q1 = ttk.OptionMenu(self, self.option_Q1_v, "168.00", "84.00", "168.00")
        self.entry_Q2 = ttk.Entry(self)
        self.entry_S = ttk.Entry(self)
        self.entry_upa = ttk.Entry(self)

        self.label_W_unit = ttk.Label(self, text="m")
        self.label_H_unit = ttk.Label(self, text="m")
        self.label_w_unit = ttk.Label(self, text="m")
        self.label_h_unit = ttk.Label(self, text="m")
        self.label_Q1_unit = ttk.Label(self, text="kW/m²")
        self.label_Q2_unit = ttk.Label(self, text="kW/m²")
        self.label_S_unit = ttk.Label(self, text="m")
        self.label_upa_unit = ttk.Label(self, text="%")

        # Set Grid Location
        # -----------------

        self.checkbutton_centered.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.checkbutton_to_boundary.grid(row=3, column=0, sticky="w", padx=10, pady=(0, 10))

        row0 = 4
        col0 = 0
        self.label_W.grid(row=row0 + 0, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_H.grid(row=row0 + 1, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_m.grid(row=row0 + 2, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_n.grid(row=row0 + 3, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_Q1.grid(row=row0 + 4, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_Q2.grid(row=row0 + 5, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_S.grid(row=row0 + 6, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_upa.grid(row=row0 + 7, column=col0 + 0, sticky="w", padx=(10, 0))

        self.entry_W.grid(row=row0 + 0, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_H.grid(row=row0 + 1, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_m.grid(row=row0 + 2, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_n.grid(row=row0 + 3, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_Q1.grid(row=row0 + 4, column=col0 + 1, sticky='ew', padx=(0, 10))
        # self.option_Q1.grid(row=row0 + 4, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_Q2.grid(row=row0 + 5, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_S.grid(row=row0 + 6, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_upa.grid(row=row0 + 7, column=col0 + 1, sticky="ew", padx=(0, 10))

        self.label_W_unit.grid(row=row0 + 0, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_H_unit.grid(row=row0 + 1, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_w_unit.grid(row=row0 + 2, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_h_unit.grid(row=row0 + 3, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_Q1_unit.grid(row=row0 + 4, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_Q2_unit.grid(row=row0 + 5, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_S_unit.grid(row=row0 + 6, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_upa_unit.grid(row=row0 + 7, column=col0 + 2, sticky="w", padx=(10, 0))

        # Set Dimension
        # -------------

        self.entry_W.config(width=9)
        self.entry_H.config(width=9)
        self.entry_m.config(width=9)
        self.entry_n.config(width=9)
        self.entry_Q1.config(width=9)
        # self.option_Q1.config(width=9)
        self.entry_Q2.config(width=9)
        self.entry_S.config(width=9)
        self.entry_upa.config(width=9)

        # Set default value
        # -----------------
        self.entry_Q1.delete(0, tk.END)
        self.entry_Q1.insert(tk.END, '187.00')

        # Output and calculate button
        # ===========================

        self.entry_upa.config(stat="readonly")
        self.entry_upa.delete(0, tk.END)

        self.button_calculate = ttk.Button(
            self, text="Calculate", command=self.calculate_resultant_heat_flux
        )
        self.button_calculate.grid(
            row=12, column=1, columnspan=2, sticky="we", padx=(0, 10), pady=10
        )

    def calculate_resultant_heat_flux(self, _=None):
        """
        Yan FU, 23 Nov 2019
        Calculates and outputs the resultant heat flux at the exposed surface based on user defined inputs from the GUI.
        :param _: Placeholder, no use. No idea why tk.Tk.root.binder would forcefully feed a parameter to the func.
        :return: No.
        """

        def update_q2_to_gui(__: str = ""):
            state = self.entry_Q2["state"]
            self.entry_Q2.config(stat=tk.NORMAL)
            self.entry_Q2.delete(0, tk.END)
            self.entry_Q2.insert(tk.END, __)
            self.entry_Q2["state"] = state

        def update_upa_to_gui(__: str = ""):
            state = self.entry_upa["state"]
            self.entry_upa.delete(0, tk.END)
            self.entry_upa.insert(tk.END, __)
            self.entry_upa.config(state="readonly")
            self.entry_upa["state"] = state

        def get_float_from_entry(list_entries_: typing.List[ttk.Entry]):
            list_entry_v = list()
            for i in list_entries_:
                try:
                    list_entry_v.append(float(i.get()))
                except:
                    list_entry_v.append(None)
            return list_entry_v

        list_label = [
            self.label_W,
            self.label_H,
            self.label_m,
            self.label_n,
            self.label_Q1,
            self.label_Q2,
            self.label_S,
            self.label_upa,
        ]
        list_entry = [
            self.entry_W,
            self.entry_H,
            self.entry_m,
            self.entry_n,
            self.entry_Q1,
            self.entry_Q2,
            self.entry_S,
            self.entry_upa,
        ]
        list_entry_v = get_float_from_entry(list_entry)

        print("BEFORE CALCULATION")
        print(
            "\n".join(
                "{:40.40} {}".format(v.cget("text") + ":", list_entry_v[i])
                for i, v in enumerate(list_label)
            )
        )

        W, H, m, n, Q1, Q2, S, upa = tuple(list_entry_v)

        # if self.checkbutton_centered_v.get() == 1:
        #     m, n = 0.5 * W, 0.5 * H
        m = 0.5 * W if self.checkbutton_centered_v.get() == 1 else m
        n = 0.5 * H if self.checkbutton_centered_v.get() == 1 else n
        S = 2.0 * S if self.checkbutton_to_boundary_v.get() == 1 else S

        # calculate heat flux at receiver, Q2
        try:
            Q2_calculated = (
                phi_parallel_any_br187(W_m=W, H_m=H, w_m=m, h_m=n, S_m=S) * Q1
            )
        except Exception as e:
            if hasattr(e, "message"):
                e = e.message
            update_upa_to_gui(e)
            return 0

        if Q2 is None:
            # if Q2 not provided, update
            Q2 = Q2_calculated
            upa = ""
        else:
            # calculate upa
            upa = min([Q2 / Q2_calculated * 100, 100])

        print("AFTER CALCULATION")
        print(
            "\n".join(
                "{:40.40} {}".format(v.cget("text") + ":", list_entry_v[i])
                for i, v in enumerate(list_label)
            )
        )

        # Update Entries
        # --------------
        # store Entry state, to restore later
        list_tk = [
            self.entry_W,
            self.entry_H,
            self.entry_m,
            self.entry_n,
            self.entry_S,
            self.entry_Q2,
            self.entry_upa,
        ]
        list_tk_states = [i["state"] for i in list_tk]

        # set Entry state to 'normal' to able to write value
        for i in list_tk:
            i["state"] = "normal"
            i.delete(0, tk.END)

        # delete existing Entry value
        for i in list_entry:
            i.delete(0, tk.END)

        # set Entry value to new values
        S = S / 2 if self.checkbutton_to_boundary_v.get() == 1 else S
        self.entry_W.insert(tk.END, f"{W:.2f}")
        self.entry_H.insert(tk.END, f"{H:.2f}")
        self.entry_m.insert(tk.END, f"{m:.2f}")
        self.entry_n.insert(tk.END, f"{n:.2f}")
        self.entry_S.insert(tk.END, f"{S:.2f}")
        self.entry_Q1.insert(tk.END, f'{Q1:.2f}')
        self.entry_Q2.insert(tk.END, f"{Q2:.2f}")
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
            self.label_h_unit.config(state="disabled", foreground="grey")
            self.label_w_unit.config(state="disabled", foreground="grey")
            self.entry_n.config(state="disabled", foreground="grey")
            self.entry_m.config(state="disabled", foreground="grey")
        elif self.checkbutton_centered_v.get() == 0:
            self.label_n.config(state="normal", foreground="black")
            self.label_m.config(state="normal", foreground="black")
            self.label_h_unit.config(state="normal", foreground="black")
            self.label_w_unit.config(state="normal", foreground="black")
            self.entry_n.config(state="normal", foreground="black")
            self.entry_m.config(state="normal", foreground="black")
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")

    def check_to_boundary(self):
        if self.checkbutton_to_boundary_v.get() == 1:
            self.label_S.config(text="½S, separation to boundary")
        elif self.checkbutton_to_boundary_v.get() == 0:
            self.label_S.config(text="S, separation to surface")
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")


class CalculatorPerpendicularlPanels(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # General App Setting
        # ===================
        self.app_name = "B4 BR187 Calculator"  # app name
        self.app_version = _ver  # app version
        self.app_description = """
        Thermal radiation calculator for\nparallel and perpendicular faced\nemitter and receiver pair.
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
        _, fp_radiation_figure_image = tempfile.mkstemp()
        with open(fp_radiation_figure_image, "wb") as f:
            f.write(base64.b64decode(OFR_LOGO_LARGE_PNG_BASE64))

        label_logo_image = Image.open(os.path.realpath(fp_radiation_figure_image))
        label_logo_image = label_logo_image.resize(
            (150, int(150 / 2.43)), Image.ANTIALIAS
        )
        label_logo_image = ImageTk.PhotoImage(label_logo_image)
        self.label_lage_logo = ttk.Label(self, image=label_logo_image)
        self.label_lage_logo.image = label_logo_image
        self.label_lage_logo.grid(row=0, column=1, columnspan=2, sticky="ne", padx=10, pady=10)

        # Short description
        # -----------------
        description_str = '\n'.join([self.app_name, self.app_version, '', self.app_description.strip()])
        self.label_short_description = ttk.Label(
            self, text=description_str, anchor="e", foreground="grey"
        )
        self.label_short_description.grid(
            row=0, column=0, sticky="w", padx=10, pady=10
        )

        # Radiation figure
        # ----------------
        _, fp_logo_image = tempfile.mkstemp()
        with open(fp_logo_image, "wb") as f:
            f.write(base64.b64decode(PERPENDICULAR_LARGE_FIGURE_PNG_BASE64))

        label_logo_image = Image.open(os.path.realpath(fp_logo_image))
        label_logo_image = label_logo_image.resize(
            (400, int(400 / 1.010)), Image.ANTIALIAS
        )
        label_logo_image = ImageTk.PhotoImage(label_logo_image)
        self.label_lage_logo = ttk.Label(self, image=label_logo_image)
        self.label_lage_logo.image = label_logo_image
        self.label_lage_logo.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Input
        # =====

        # Create Objects
        # --------------

        self.checkbutton_centered_v = tk.IntVar(value=1)  # set default, receiver to the center of emitter
        self.checkbutton_centered = ttk.Checkbutton(self, text="Centered receiver", variable=self.checkbutton_centered_v, command=self.check_center_receiver)
        self.checkbutton_to_boundary_v = tk.IntVar(value=1)  # set default, separation to notional boundary
        self.checkbutton_to_boundary = ttk.Checkbutton(self, text="Separation to boundary", variable=self.checkbutton_to_boundary_v, command=self.check_to_boundary, )

        self.label_W = ttk.Label(self, text="W, emitter width")
        self.label_H = ttk.Label(self, text="H, emitter height")
        self.label_m = ttk.Label(self, text="m, receiver width")
        self.label_n = ttk.Label(self, text="n, receiver height")
        self.label_Q1 = ttk.Label(self, text="Q1, emitter HT (84, 168)")
        self.label_Q2 = ttk.Label(self, text="Q2, permitted HT (optional, 12.6)")
        self.label_S = ttk.Label(self, text="S, separation")
        self.label_upa = ttk.Label(self, text="Calculated Permitted UPA")

        self.entry_W = ttk.Entry(self)
        self.entry_H = ttk.Entry(self)
        self.entry_m = ttk.Entry(self)
        self.entry_n = ttk.Entry(self)
        self.entry_Q1 = ttk.Entry(self)
        # self.option_Q1_v = tk.StringVar(self.master)
        # self.option_Q1_v.set("168.00")
        # self.option_Q1 = ttk.OptionMenu(self, self.option_Q1_v, "168.00", "84.00", "168.00")
        self.entry_Q2 = ttk.Entry(self)
        self.entry_S = ttk.Entry(self)
        self.entry_upa = ttk.Entry(self)

        self.label_W_unit = ttk.Label(self, text="m")
        self.label_H_unit = ttk.Label(self, text="m")
        self.label_w_unit = ttk.Label(self, text="m")
        self.label_h_unit = ttk.Label(self, text="m")
        self.label_Q1_unit = ttk.Label(self, text="kW/m²")
        self.label_Q2_unit = ttk.Label(self, text="kW/m²")
        self.label_S_unit = ttk.Label(self, text="m")
        self.label_upa_unit = ttk.Label(self, text="%")

        # Set Grid Location
        # -----------------

        self.checkbutton_centered.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.checkbutton_to_boundary.grid(row=3, column=0, sticky="w", padx=10, pady=(0, 10))

        row0 = 4
        col0 = 0
        self.label_W.grid(row=row0 + 0, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_H.grid(row=row0 + 1, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_m.grid(row=row0 + 2, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_n.grid(row=row0 + 3, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_Q1.grid(row=row0 + 4, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_Q2.grid(row=row0 + 5, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_S.grid(row=row0 + 6, column=col0 + 0, sticky="w", padx=(10, 0))
        self.label_upa.grid(row=row0 + 7, column=col0 + 0, sticky="w", padx=(10, 0))

        self.entry_W.grid(row=row0 + 0, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_H.grid(row=row0 + 1, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_m.grid(row=row0 + 2, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_n.grid(row=row0 + 3, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_Q1.grid(row=row0 + 4, column=col0 + 1, sticky='ew', padx=(0, 10))
        # self.option_Q1.grid(row=row0 + 4, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_Q2.grid(row=row0 + 5, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_S.grid(row=row0 + 6, column=col0 + 1, sticky="ew", padx=(0, 10))
        self.entry_upa.grid(row=row0 + 7, column=col0 + 1, sticky="ew", padx=(0, 10))

        self.label_W_unit.grid(row=row0 + 0, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_H_unit.grid(row=row0 + 1, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_w_unit.grid(row=row0 + 2, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_h_unit.grid(row=row0 + 3, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_Q1_unit.grid(row=row0 + 4, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_Q2_unit.grid(row=row0 + 5, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_S_unit.grid(row=row0 + 6, column=col0 + 2, sticky="w", padx=(10, 0))
        self.label_upa_unit.grid(row=row0 + 7, column=col0 + 2, sticky="w", padx=(10, 0))

        # Set Dimension
        # -------------

        self.entry_W.config(width=9)
        self.entry_H.config(width=9)
        self.entry_m.config(width=9)
        self.entry_n.config(width=9)
        self.entry_Q1.config(width=9)
        # self.option_Q1.config(width=9)
        self.entry_Q2.config(width=9)
        self.entry_S.config(width=9)
        self.entry_upa.config(width=9)

        # Set default value
        # -----------------
        self.entry_Q1.delete(0, tk.END)
        self.entry_Q1.insert(tk.END, '187.00')

        # Output and calculate button
        # ===========================

        self.entry_upa.config(stat="readonly")
        self.entry_upa.delete(0, tk.END)

        self.button_calculate = ttk.Button(
            self, text="Calculate", command=self.calculate_resultant_heat_flux
        )
        self.button_calculate.grid(
            row=12, column=1, columnspan=2, sticky="we", padx=(0, 10), pady=10
        )

    def calculate_resultant_heat_flux(self, _=None):
        """
        Yan FU, 26 Nov 2019
        Calculates and outputs the resultant heat flux at the exposed surface based on user defined inputs from the GUI.
        :param _: Placeholder, no use. No idea why tk.Tk.root.binder would forcefully feed a parameter to the func.
        :return: No.
        """

        def update_upa_to_gui(__: str = ""):
            state = self.entry_upa["state"]
            self.entry_upa.delete(0, tk.END)
            self.entry_upa.insert(tk.END, __)
            self.entry_upa.config(state="readonly")
            self.entry_upa["state"] = state

        def get_float_from_entry(list_entries_: typing.List[ttk.Entry]):
            list_entry_v = list()
            for i in list_entries_:
                try:
                    list_entry_v.append(float(i.get()))
                except:
                    list_entry_v.append(None)
            return list_entry_v

        list_label = [
            self.label_W,
            self.label_H,
            self.label_m,
            self.label_n,
            self.label_Q1,
            self.label_Q2,
            self.label_S,
            self.label_upa,
        ]
        list_entry = [
            self.entry_W,
            self.entry_H,
            self.entry_m,
            self.entry_n,
            self.entry_Q1,
            self.entry_Q2,
            self.entry_S,
            self.entry_upa,
        ]
        list_entry_v = get_float_from_entry(list_entry)

        print("BEFORE CALCULATION")
        print(
            "\n".join(
                "{:40.40} {}".format(v.cget("text") + ":", list_entry_v[i])
                for i, v in enumerate(list_label)
            )
        )

        W, H, m, n, Q1, Q2, S, upa = tuple(list_entry_v)

        # if self.checkbutton_centered_v.get() == 1:
        #     m, n = 0.5 * W, 0.5 * H
        m = 0.5 * W if self.checkbutton_centered_v.get() == 1 else m
        n = 0.5 * H if self.checkbutton_centered_v.get() == 1 else n
        S = 2.0 * S if self.checkbutton_to_boundary_v.get() == 1 else S

        # calculate heat flux at receiver, Q2
        try:
            Q2_calculated = (
                phi_perpendicular_any_br187(W_m=W, H_m=H, w_m=m, h_m=n, S_m=S) * Q1
            )
        except Exception as e:
            if hasattr(e, "message"):
                e = e.message
            update_upa_to_gui(e)
            return 0

        if Q2 is None:
            # if Q2 not provided, update
            Q2 = Q2_calculated
            upa = ""
        else:
            # calculate upa
            upa = min([Q2 / Q2_calculated * 100, 100])

        print("AFTER CALCULATION")
        print(
            "\n".join(
                "{:40.40} {}".format(v.cget("text") + ":", list_entry_v[i])
                for i, v in enumerate(list_label)
            )
        )

        # Update Entries
        # --------------
        # store Entry state, to restore later
        list_tk = [
            self.entry_W,
            self.entry_H,
            self.entry_m,
            self.entry_n,
            self.entry_S,
            self.entry_Q2,
            self.entry_upa,
        ]
        list_tk_states = [i["state"] for i in list_tk]

        # set Entry state to 'normal' to able to write value
        for i in list_tk:
            i["state"] = "normal"
            i.delete(0, tk.END)

        # delete existing Entry value
        for i in list_entry:
            i.delete(0, tk.END)

        # set Entry value to new values
        S = S / 2 if self.checkbutton_to_boundary_v.get() == 1 else S
        self.entry_W.insert(tk.END, f"{W:.2f}")
        self.entry_H.insert(tk.END, f"{H:.2f}")
        self.entry_m.insert(tk.END, f"{m:.2f}")
        self.entry_n.insert(tk.END, f"{n:.2f}")
        self.entry_S.insert(tk.END, f"{S:.2f}")
        self.entry_Q1.insert(tk.END, f'{Q1:.2f}')
        self.entry_Q2.insert(tk.END, f"{Q2:.2f}")
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
            self.label_h_unit.config(state="disabled", foreground="grey")
            self.label_w_unit.config(state="disabled", foreground="grey")
            self.entry_n.config(state="disabled", foreground="grey")
            self.entry_m.config(state="disabled", foreground="grey")
        elif self.checkbutton_centered_v.get() == 0:
            self.label_n.config(state="normal", foreground="black")
            self.label_m.config(state="normal", foreground="black")
            self.label_h_unit.config(state="normal", foreground="black")
            self.label_w_unit.config(state="normal", foreground="black")
            self.entry_n.config(state="normal", foreground="black")
            self.entry_m.config(state="normal", foreground="black")
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")

    def check_to_boundary(self):
        if self.checkbutton_to_boundary_v.get() == 1:
            self.label_S.config(text="½S, separation to boundary")
        elif self.checkbutton_to_boundary_v.get() == 0:
            self.label_S.config(text="S, separation to surface")
        else:
            raise ValueError("Unknown tk.ttk.CheckButton value.")


def main():
    my_gui = Calculator()
    my_gui.mainloop()


if __name__ == "__main__":
    main()
