import tkinter as tk
from tkinter import ttk
from fseutil.lib.fse_thermal_radiation_gui import Calculator
from multiprocessing import Process


class MainWindow(tk.Tk):

    process_pool = list()

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('OFR FSE Utility Application')

        self.protocol("WM_DELETE_WINDOW", self.clean_processes)

        self.button_calculator_b4 = ttk.Button(self, text="BR 187 Radiation Calculator", command=self.calculator_b4)
        self.button_calculator_b4.grid(row=0, column=0, columnspan=1, sticky="nswe", padx=10, pady=5)

        self.mainloop()

    def clean_processes(self):
        for i in self.process_pool:
            try:
                i.kill()
            except:
                pass
        self.destroy()

    def calculator_b4(self):
        p = Process(target=Calculator, args=())
        p.start()
        self.process_pool.append(p)


if __name__ == "__main__":
    main = MainWindow()
