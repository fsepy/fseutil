import base64
import tempfile
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import typing
from fseutil import __version__ as _ver

from fseutil.lib.fse_b4_br187 import phi_parallel_any_br187
from fseutil.etc.b4_br187 import RADIATION_FIGURE_PNG_BASE64, OFR_LOGO_LARGE_PNG_BASE64, OFR_LOGO_SMALL_PNG_BASE64


class Calculator(ttk.Frame):

    def __init__(self, root: tk.Tk = None):
        super().__init__()

        self.app_name = 'OFR B4 BR187 Calculator'

        if root:
            root.bind(sequence='<Return>', func=self.calculate_resultant_heat_flux)

        # Instantiate GUI objects
        # -----------------------

        self.label_logo = None

        self.text_short_description = None

        self.checkbutton_centered: ttk.Checkbutton
        self.checkbutton_centered_v = tk.IntVar(value=1)

        self.checkbutton_upa: ttk.Checkbutton
        self.checkbutton_upa_v = tk.IntVar(value=1)

        self.checkbutton_to_boudnary: ttk.Checkbutton
        self.checkbutton_to_boudnary_v = tk.IntVar(value=1)

        self.label_W: ttk.Label
        self.entry_W: ttk.Entry
        self.label_H: ttk.Label
        self.entry_H: ttk.Entry
        self.label_m: ttk.Label
        self.entry_m: ttk.Entry
        self.label_n: ttk.Label
        self.entry_n: ttk.Entry
        self.label_S: ttk.Label
        self.entry_S: ttk.Entry
        self.label_Q1: ttk.Label
        self.entry_Q1: ttk.Entry
        self.label_Q2: ttk.Label
        self.entry_Q2: ttk.Entry
        self.label_upa: ttk.Label
        self.entry_upa: ttk.Entry

        self.button_calculate: ttk.Button

        self.init_ui()

        self.check_center_receiver()
        self.check_to_boundary()

        self.master.resizable(0, 0)

    def init_ui(self):

        # SETTINGS
        # ========

        # set icon to .exe file
        _, fp_icon = tempfile.mkstemp()
        with open(fp_icon, "wb") as f:
            f.write(base64.b64decode(OFR_LOGO_SMALL_PNG_BASE64))
        self.master.iconbitmap(fp_icon)

        # set dialog header title
        self.master.title(self.app_name)

        self.pack(fill=tk.BOTH, expand=True)

        self.columnconfigure(1, pad=2)

        # STYLES
        # ======
        style = ttk.Style()
        style.configure("TLabel", foreground="black", background="white", font=("Helvetica", 17))
        style.configure("TCheckButton", foreground="black", background="white", font=("Helvetica", 17))

        # GUI LAYOUT
        # ==========

        # Large logo
        # ----------
        _, fp_radiation_figure_image = tempfile.mkstemp()
        with open(fp_radiation_figure_image, "wb") as f:
            f.write(base64.b64decode(OFR_LOGO_LARGE_PNG_BASE64))
        self.master.iconbitmap(fp_radiation_figure_image)

        label_logo_image = Image.open(os.path.realpath(fp_radiation_figure_image))
        label_logo_image = label_logo_image.resize((150, int(150/2.43)), Image.ANTIALIAS)
        label_logo_image = ImageTk.PhotoImage(label_logo_image)
        self.label_logo = ttk.Label(self, image=label_logo_image)
        self.label_logo.image = label_logo_image
        self.label_logo.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        # Short description
        # -----------------
        description_str = f'OFR B4 BR187 Calculator\n{_ver}'
        self.text_short_description = ttk.Label(self, text=description_str, anchor='e', foreground='grey', font=("Helvetica", 15))
        self.text_short_description.grid(row=0, column=1, columnspan=2, sticky='wens', padx=5, pady=5)

        # Radiation figure
        # ----------------
        _, fp_logo_image = tempfile.mkstemp()
        with open(fp_logo_image, "wb") as f:
            f.write(base64.b64decode(RADIATION_FIGURE_PNG_BASE64))
        self.master.iconbitmap(fp_logo_image)

        label_logo_image = Image.open(os.path.realpath(fp_logo_image))
        label_logo_image = label_logo_image.resize((400, int(400/1.010)), Image.ANTIALIAS)
        label_logo_image = ImageTk.PhotoImage(label_logo_image)
        self.label_logo = ttk.Label(self, image=label_logo_image)
        self.label_logo.image = label_logo_image
        self.label_logo.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Input
        # -----
        # create objects
        self.checkbutton_centered = ttk.Checkbutton(
            self,
            text='Centered receiver',
            variable=self.checkbutton_centered_v,
            command=self.check_center_receiver
        )

        self.checkbutton_to_boudnary = ttk.Checkbutton(
            self,
            text='Separation to boundary',
            variable=self.checkbutton_to_boudnary_v,
            command=self.check_to_boundary
        )

        self.label_W = ttk.Label(self, text='W, emitter width')
        self.label_H = ttk.Label(self, text='H, emitter height')
        self.label_m = ttk.Label(self, text='m, receiver width')
        self.label_n = ttk.Label(self, text='n, receiver height')
        self.label_S = ttk.Label(self, text='S, separation')
        self.label_Q1 = ttk.Label(self, text='Q1, emitter HT (84, 168)')
        self.label_Q2 = ttk.Label(self, text='Q2, permitted HT (optional, 12.6)')
        self.label_upa = ttk.Label(self, text='Calculated Permitted UPA')

        self.entry_W = ttk.Entry(self)
        self.entry_H = ttk.Entry(self)
        self.entry_m = ttk.Entry(self)
        self.entry_n = ttk.Entry(self)
        self.entry_S = ttk.Entry(self)
        self.entry_Q1 = ttk.Entry(self)
        self.entry_Q2 = ttk.Entry(self)
        self.entry_upa = ttk.Entry(self)

        self.label_W_unit = ttk.Label(self, text='m')
        self.label_H_unit = ttk.Label(self, text='m')
        self.label_w_unit = ttk.Label(self, text='m')
        self.label_h_unit = ttk.Label(self, text='m')
        self.label_S_unit = ttk.Label(self, text='m')
        self.label_Q1_unit = ttk.Label(self, text='kW/m²')
        self.label_Q2_unit = ttk.Label(self, text='kW/m²')
        self.label_upa_unit = ttk.Label(self, text='%')

        # set grid location
        self.checkbutton_centered.grid(row=2, column=0, sticky='w', padx=5, pady=(5, 0))
        self.checkbutton_to_boudnary.grid(row=3, column=0, sticky='w', padx=5, pady=(0, 5))

        row0 = 4
        col0 = 0
        self.label_W.grid(row=row0+0, column=col0+0, sticky='w', padx=(5, 0))
        self.label_H.grid(row=row0+1, column=col0+0, sticky='w', padx=(5, 0))
        self.label_m.grid(row=row0 + 2, column=col0 + 0, sticky='w', padx=(5, 0))
        self.label_n.grid(row=row0 + 3, column=col0 + 0, sticky='w', padx=(5, 0))
        self.label_S.grid(row=row0+4, column=col0+0, sticky='w', padx=(5, 0))
        self.label_Q1.grid(row=row0 + 5, column=col0 + 0, sticky='w', padx=(5, 0))
        self.label_Q2.grid(row=row0 + 6, column=col0 + 0, sticky='w', padx=(5, 0))
        self.label_upa.grid(row=row0 + 7, column=col0 + 0, sticky='w', padx=(5, 0))

        self.entry_W.grid(row=row0+0, column=col0+1, sticky='e', padx=(0, 5))
        self.entry_H.grid(row=row0+1, column=col0+1, sticky='e', padx=(0, 5))
        self.entry_m.grid(row=row0 + 2, column=col0 + 1, sticky='e', padx=(0, 5))
        self.entry_n.grid(row=row0 + 3, column=col0 + 1, sticky='e', padx=(0, 5))
        self.entry_S.grid(row=row0+4, column=col0+1, sticky='e', padx=(0, 5))
        self.entry_Q1.grid(row=row0 + 5, column=col0 + 1, sticky='e', padx=(0, 5))
        self.entry_Q2.grid(row=row0 + 6, column=col0 + 1, sticky='e', padx=(0, 5))
        self.entry_upa.grid(row=row0 + 7, column=col0 + 1, sticky='e', padx=(0, 5))

        self.label_W_unit.grid(row=row0+0, column=col0+2, sticky='w', padx=(5, 0))
        self.label_H_unit.grid(row=row0+1, column=col0+2, sticky='w', padx=(5, 0))
        self.label_w_unit.grid(row=row0+2, column=col0+2, sticky='w', padx=(5, 0))
        self.label_h_unit.grid(row=row0+3, column=col0+2, sticky='w', padx=(5, 0))
        self.label_S_unit.grid(row=row0+4, column=col0+2, sticky='w', padx=(5, 0))
        self.label_Q1_unit.grid(row=row0 + 5, column=col0+2, sticky='w', padx=(5, 0))
        self.label_Q2_unit.grid(row=row0 + 6, column=col0+2, sticky='w', padx=(5, 0))
        self.label_upa_unit.grid(row=row0 + 7, column=col0+2, sticky='w', padx=(5, 0))

        # set dimension
        self.entry_W.config(width=9)
        self.entry_H.config(width=9)
        self.entry_m.config(width=9)
        self.entry_n.config(width=9)
        self.entry_S.config(width=9)
        self.entry_Q1.config(width=9)
        self.entry_Q2.config(width=9)
        self.entry_upa.config(width=9)

        # Output and calculate button
        # ---------------------------
        self.entry_upa.config(stat='readonly')
        self.entry_upa.delete(0, tk.END)

        self.button_calculate = ttk.Button(self, text="Calculate", command=self.calculate_resultant_heat_flux)
        self.button_calculate.grid(row=12, column=1, columnspan=2, sticky='e', padx=5, pady=(0, 5))

    def calculate_resultant_heat_flux(self, _=None):
        """
        Yan FU, 23 Nov 2019
        Calculates and outputs the resultant heat flux at the exposed surface based on user defined inputs from the GUI.
        :param _: Placeholder, no use. No idea why tk.Tk.root.binder would forcefully feed a parameter to the func.
        :return: No.
        """

        def update_q2_to_gui(__: str = ''):
            self.entry_Q2.config(stat=tk.NORMAL)
            self.entry_Q2.delete(0, tk.END)
            self.entry_Q2.insert(tk.END, __)
            self.entry_Q2.config(state='readonly')

        def update_upa_to_gui(__: str = ''):
            self.entry_upa.config(stat=tk.NORMAL)
            self.entry_upa.delete(0, tk.END)
            self.entry_upa.insert(tk.END, __)
            self.entry_upa.config(state='readonly')

        def get_float_from_entry(list_entries_: typing.List[ttk.Entry]):
            list_entry_v = list()
            for i in list_entries_:
                try:
                    list_entry_v.append(float(i.get()))
                except:
                    list_entry_v.append(None)

            return list_entry_v

        list_entry = [self.entry_W, self.entry_H, self.entry_m, self.entry_n, self.entry_S, self.entry_Q1, self.entry_Q2]
        list_entry_v = get_float_from_entry(list_entry)

        W, H, m, n, S, Q1, Q2 = tuple(list_entry_v)
        m = 0.5 * W if m is None else 0.5 * W
        n = 0.5 * H if n is None else 0.5 * H
        S = 2.0 * S if self.checkbutton_to_boudnary_v.get() == 1 else S
        print(S)

        try:
            Q2_calculated = phi_parallel_any_br187(W_m=W, H_m=H, w_m=m, h_m=n, S_m=S) * Q1
        except Exception as e:
            if hasattr(e, 'message'):
                e = e.message
            update_upa_to_gui(e)
            return 0

        if Q2 is None:
            update_q2_to_gui(f'{Q2_calculated:.3f}')
            return 0

        # calculate upa
        upa = min([Q2 / Q2_calculated * 100, 100])
        update_upa_to_gui(f'{upa:.1f}')

        # update inputs
        list_tk = [self.entry_W, self.entry_H, self.entry_m, self.entry_n, self.entry_S]
        list_tk_states = [i['state'] for i in list_tk]
        for i in list_tk:
            i['state'] = 'normal'
            i.delete(0, tk.END)

        for i in list_entry:
            i.delete(0, tk.END)

        S = S / 2 if self.checkbutton_to_boudnary_v.get() == 1 else S

        self.entry_W.insert(tk.END, f'{W:.2f}')
        self.entry_H.insert(tk.END, f'{H:.2f}')
        self.entry_m.insert(tk.END, f'{m:.2f}')
        self.entry_n.insert(tk.END, f'{n:.2f}')
        self.entry_S.insert(tk.END, f'{S:.2f}')
        self.entry_Q1.insert(tk.END, f'{Q1:.2f}')
        self.entry_Q2.insert(tk.END, f'{Q2:.2f}')

        for i, v in enumerate(list_tk):
            v['state'] = list_tk_states[i]


        # update results

    def check_center_receiver(self):
        if self.checkbutton_centered_v.get() == 1:
            self.label_n.config(state='disabled', foreground='grey')
            self.label_m.config(state='disabled', foreground='grey')
            self.label_h_unit.config(state='disabled', foreground='grey')
            self.label_w_unit.config(state='disabled', foreground='grey')
            self.entry_n.config(state='disabled', foreground='grey')
            self.entry_m.config(state='disabled', foreground='grey')
        elif self.checkbutton_centered_v.get() == 0:
            self.label_n.config(state='normal', foreground='black')
            self.label_m.config(state='normal', foreground='black')
            self.label_h_unit.config(state='normal', foreground='black')
            self.label_w_unit.config(state='normal', foreground='black')
            self.entry_n.config(state='normal', foreground='black')
            self.entry_m.config(state='normal', foreground='black')
        else:
            raise ValueError('Unknown tk.ttk.CheckButton value.')

    def check_to_boundary(self):
        if self.checkbutton_to_boudnary_v.get() == 1:
            self.label_S.config(text='½S, separation to boundary')
        elif self.checkbutton_to_boudnary_v.get() == 0:
            self.label_S.config(text='S, separation to surface')
        else:
            raise ValueError('Unknown tk.ttk.CheckButton value.')


def main():
    root = tk.Tk()
    my_gui = Calculator(root)
    root.mainloop()


if __name__ == '__main__':
    main()
