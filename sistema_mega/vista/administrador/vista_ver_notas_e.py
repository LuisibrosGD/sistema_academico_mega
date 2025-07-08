import tkinter as tk
import os
import pandas as pd

from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from sistema_mega.modelo.ver_notas_estudiante import (
    obtener_sedes,
    obtener_ciclos,
    obtener_grupos,
    obtener_notas_filtradas
)

class VistaNotasEstudiantes(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Notas de Estudiantes - Año Actual")
        self.geometry("1400x800")
        self.configure(bg='#f0f0f0')
        self.datos_filtrados = []

        self.create_widgets()
        self.load_filters()

    def create_widgets(self):
        title_label = tk.Label(self, text="Notas de Estudiantes - Año Actual",
                               font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=15)

        filter_frame = tk.Frame(self, bg='#f0f0f0')
        filter_frame.pack(pady=10)

        self.sede_cb = self.create_combobox(filter_frame, "Sede:", 0)
        self.ciclo_cb = self.create_combobox(filter_frame, "Ciclo:", 1)
        self.grupo_cb = self.create_combobox(filter_frame, "Grupo:", 2)
        self.area_cb = self.create_combobox(filter_frame, "Área Académica:", 3, values=["", "A", "B", "C", "D", "E"])

        tk.Label(filter_frame, text="Fecha Inicio:", bg='#f0f0f0').grid(row=1, column=0, padx=5, pady=5)
        self.fecha_inicio = DateEntry(filter_frame, width=12, date_pattern='yyyy-mm-dd',
                                      background='darkblue', foreground='white', borderwidth=2)
        self.fecha_inicio.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Fecha Fin:", bg='#f0f0f0').grid(row=1, column=2, padx=5, pady=5)
        self.fecha_fin = DateEntry(filter_frame, width=12, date_pattern='yyyy-mm-dd',
                                   background='darkblue', foreground='white', borderwidth=2)
        self.fecha_fin.grid(row=1, column=3, padx=5, pady=5)

        buscar_btn = tk.Button(filter_frame, text="Filtrar", bg="#007bff", fg="white", command=self.buscar_notas)
        buscar_btn.grid(row=1, column=4, padx=10, pady=5)

        self.export_btn = tk.Button(filter_frame, text="Exportar a Excel", bg="#28a745", fg="white",
                                    command=self.exportar_excel, state=tk.DISABLED)
        self.export_btn.grid(row=1, column=5, padx=5, pady=5)

        self.create_table()

        btn_frame = tk.Frame(self, bg='#f0f0f0')
        btn_frame.pack(fill=tk.X, pady=10)

        btn_menu = tk.Button(btn_frame, text="Regresar a Menú principal",
                             bg='#6c757d', fg='white', font=("Arial", 10),
                             padx=20, pady=5, command=self.go_to_main_menu)
        btn_menu.pack(side=tk.LEFT, padx=10)

    def create_combobox(self, parent, label, col, values=None):
        tk.Label(parent, text=label, bg='#f0f0f0').grid(row=0, column=col * 2, padx=5, pady=5)
        cb = ttk.Combobox(parent, width=20, values=values or [])
        cb.grid(row=0, column=col * 2 + 1, padx=5, pady=5)
        return cb

    def create_table(self):
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ('Sede', 'Ciclo', 'Grupo', 'Nombre Completo', 'Área Académica', 'Nota', 'Fecha')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_filters(self):
        self.sede_cb['values'] = [""] + [s['nombre'] for s in obtener_sedes()]
        self.ciclo_cb['values'] = [""] + [c['nombre_ciclo'] for c in obtener_ciclos()]
        self.grupo_cb['values'] = [""] + [g['nombre_grupo'] for g in obtener_grupos()]

    def buscar_notas(self):
        filtros = {
            'sede': self.sede_cb.get(),
            'ciclo': self.ciclo_cb.get(),
            'grupo': self.grupo_cb.get(),
            'area_academica': self.area_cb.get().lower(),
            'fecha_inicio': self.fecha_inicio.get(),
            'fecha_fin': self.fecha_fin.get()
        }

        try:
            notas = obtener_notas_filtradas(filtros)
            self.datos_filtrados = notas  # 👉 Guarda los datos para exportar

            for item in self.tree.get_children():
                self.tree.delete(item)

            for n in notas:
                self.tree.insert('', tk.END, values=(
                    n['sede'],
                    n['ciclo'],
                    n['grupo'],
                    n['nombre_completo'],
                    n['area_academica'].upper(),
                    f"{n['nota']:.2f}",
                    n['fecha']
                ))

            if not notas:
                messagebox.showinfo("Sin resultados", "No se encontraron notas con esos filtros.")
                self.export_btn.config(state=tk.DISABLED)
            else:
                self.export_btn.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al buscar notas:\n{str(e)}")

    def go_to_main_menu(self):
        if messagebox.askyesno("Confirmar", "¿Desea regresar al menú principal?"):
            self.destroy()
            self.parent.deiconify()

    def exportar_excel(self):
        if not self.datos_filtrados:
            messagebox.showwarning("Sin datos", "No hay datos para exportar.")
            return

        try:
            os.makedirs("registro_notas", exist_ok=True)

            df = pd.DataFrame(self.datos_filtrados)
            archivo = os.path.join("registro_notas", "notas_filtradas.xlsx")
            df.to_excel(archivo, index=False)

            messagebox.showinfo("Exportado", f"Notas exportadas exitosamente a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error al exportar", f"No se pudo exportar a Excel:\n{str(e)}")

