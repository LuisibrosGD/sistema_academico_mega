import tkinter as tk
from tkinter import ttk
# Realizado por Luis Bizarro
class GestionColaboradores(tk.Toplevel):
    def __init__(self, ventana_anterior):
        super().__init__()

        self.ventana_anterior = ventana_anterior

        self.title("Gestion Colaboradores")
        self.geometry("800x600")
        self.centrar_ventana()


        #boton volver
        boton_volver = tk.Button(self, text="Volver", command=self.regresar_menu)
        boton_volver.pack(pady=20)

    def centrar_ventana(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def regresar_menu(self):
        self.destroy()
        self.ventana_anterior.deiconify()
