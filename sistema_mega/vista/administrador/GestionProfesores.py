import tkinter as tk
from tkinter import ttk

class GestionProfesores(tk.Toplevel):
    def __init__(self, ventana_anterior):
        super().__init__()
        self.ventana_anterior = ventana_anterior





        boton_volver = tk.Button(self, text="Volver", command=self.regresar_menu)
        boton_volver.pack(pady=20)
    def regresar_menu(self):
        self.destroy()
        self.ventana_anterior.deiconify()