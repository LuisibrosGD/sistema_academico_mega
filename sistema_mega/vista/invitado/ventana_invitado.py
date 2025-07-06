# sistema_mega/vista/invitado/ventana_invitado.py

import tkinter as tk
from tkinter import ttk

class MenuInvitado(tk.Toplevel):
    def mostrar_interfaz(self):
        super().__init__()
        self.ventana = ttk.Frame(self)
        self.ventana.title("Modo Invitado")
        self.ventana.geometry("300x200")

        label = tk.Label(ventana, text="Bienvenido, invitado", font=("Arial", 14))
        label.pack(pady=40)

        boton = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
        boton.pack(pady=10)

if __name__ == '__main__':
    app = MenuInvitado()
    app.mainloop()
