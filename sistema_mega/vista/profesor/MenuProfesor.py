import tkinter as tk
from tkinter import ttk
from sistema_mega.modelo.profesor_modelo import *


class MenuProfesor(tk.Toplevel):
    def __init__(self, id_profesor, nombre_profesor):
        super().__init__()
        self.configure(bg="grey")
        self.id_profesor = id_profesor
        self.nombre_profesor = nombre_profesor