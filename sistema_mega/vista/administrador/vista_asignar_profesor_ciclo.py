import tkinter as tk
from tkinter import ttk, messagebox
from sistema_mega.modelo.modelo_profesor_ciclo import obtener_profesores, obtener_cursos, obtener_ciclos_programados, asignar_profesor, validar_id_profesor, validar_id_curso, validar_id_ciclo

class AsignarProfesorCiclo(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Asignar Profesores a Ciclos y Especialidades")
        self.geometry("1400x900")
        self.configure(bg='#f0f0f0')

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        title_label = tk.Label(self, text="Asignar Profesores a Ciclos y Especialidades",
                               font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=15)

        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        top_frame = tk.Frame(main_frame, bg='#f0f0f0')
        top_frame.pack(fill=tk.BOTH, expand=True)

        self.create_profesores_table(top_frame)
        self.create_cursos_table(top_frame)
        self.create_ciclos_table(top_frame)

        form_frame = tk.Frame(main_frame, bg='#f8f9fa', relief=tk.RAISED, bd=1, padx=20, pady=15)
        form_frame.pack(fill=tk.X, pady=(10, 20))
        self.create_assignment_form(form_frame)

        btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
        btn_frame.pack(fill=tk.X, pady=10)

        btn_menu = tk.Button(btn_frame, text="Regresar a Menú principal",
                             bg='#6c757d', fg='white', font=("Arial", 10),
                             padx=20, pady=5, command=self.go_to_main_menu)
        btn_menu.pack(side=tk.LEFT)

    def create_profesores_table(self, parent):
        prof_frame = tk.LabelFrame(parent, text="Profesores", bg='white', fg='#333', font=("Arial", 11, "bold"))
        prof_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ('ID', 'Nombre', 'Especialidad')
        self.profesores_tree = ttk.Treeview(prof_frame, columns=columns, show='headings', height=12)
        for col in columns:
            self.profesores_tree.heading(col, text=col)
        self.profesores_tree.column('ID', width=50)
        self.profesores_tree.column('Nombre', width=150)
        self.profesores_tree.column('Especialidad', width=150)

        scrollbar = ttk.Scrollbar(prof_frame, orient=tk.VERTICAL, command=self.profesores_tree.yview)
        self.profesores_tree.configure(yscrollcommand=scrollbar.set)

        self.profesores_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_cursos_table(self, parent):
        cursos_frame = tk.LabelFrame(parent, text="Cursos", bg='white', fg='#333', font=("Arial", 11, "bold"))
        cursos_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ('ID', 'Curso')
        self.cursos_tree = ttk.Treeview(cursos_frame, columns=columns, show='headings', height=12)
        for col in columns:
            self.cursos_tree.heading(col, text=col)
        self.cursos_tree.column('ID', width=50)
        self.cursos_tree.column('Curso', width=180)

        scrollbar = ttk.Scrollbar(cursos_frame, orient=tk.VERTICAL, command=self.cursos_tree.yview)
        self.cursos_tree.configure(yscrollcommand=scrollbar.set)

        self.cursos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_ciclos_table(self, parent):
        ciclos_frame = tk.LabelFrame(parent, text="Ciclos Programados", bg='white', fg='#333', font=("Arial", 11, "bold"))
        ciclos_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ('ID', 'Sede', 'Ciclo', 'Grupo')
        self.ciclos_tree = ttk.Treeview(ciclos_frame, columns=columns, show='headings', height=12)
        for col in columns:
            self.ciclos_tree.heading(col, text=col)
        self.ciclos_tree.column('ID', width=50)
        self.ciclos_tree.column('Sede', width=100)
        self.ciclos_tree.column('Ciclo', width=120)
        self.ciclos_tree.column('Grupo', width=80)

        scrollbar = ttk.Scrollbar(ciclos_frame, orient=tk.VERTICAL, command=self.ciclos_tree.yview)
        self.ciclos_tree.configure(yscrollcommand=scrollbar.set)

        self.ciclos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_assignment_form(self, parent):
        form_title = tk.Label(parent, text="Asignar Profesor a Ciclo y Curso",
                              bg='#f8f9fa', fg='#495057', font=("Arial", 12, "bold"))
        form_title.grid(row=0, column=0, columnspan=6, pady=(0, 15))

        etiquetas = [
            ("ID Profesor:", 1, 0), ("ID Curso:", 1, 2), ("ID Ciclo:", 1, 4),
            ("Día:", 2, 0), ("Hora de Inicio:", 2, 2), ("Hora de Fin:", 2, 4)
        ]
        for texto, fila, columna in etiquetas:
            tk.Label(parent, text=texto, bg='#f8f9fa', fg='#495057').grid(row=fila, column=columna, sticky=tk.W, padx=5, pady=5)

        self.id_profesor_entry = tk.Entry(parent, width=15)
        self.id_profesor_entry.grid(row=1, column=1, padx=5, pady=5)

        self.id_curso_entry = tk.Entry(parent, width=15)
        self.id_curso_entry.grid(row=1, column=3, padx=5, pady=5)

        self.id_ciclo_entry = tk.Entry(parent, width=15)
        self.id_ciclo_entry.grid(row=1, column=5, padx=5, pady=5)

        self.dia_var = tk.StringVar(value="lunes")
        self.dia_combo = ttk.Combobox(parent, textvariable=self.dia_var, width=12,
                                 values=["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"])
        self.dia_combo.grid(row=2, column=1, padx=5, pady=5)

        horas = [f"{h:02d}:{m:02d}" for h in range(8, 22+1) for m in (0, 30)]

        self.hora_inicio_var = tk.StringVar()
        self.hora_inicio_combo = ttk.Combobox(parent, textvariable=self.hora_inicio_var, values=horas, width=12)
        self.hora_inicio_combo.set("08:00")
        self.hora_inicio_combo.grid(row=2, column=3, padx=5, pady=5)

        self.hora_fin_var = tk.StringVar()
        self.hora_fin_combo = ttk.Combobox(parent, textvariable=self.hora_fin_var, values=horas, width=12)
        self.hora_fin_combo.set("10:00")
        self.hora_fin_combo.grid(row=2, column=5, padx=5, pady=5)

        btn_frame = tk.Frame(parent, bg='#f8f9fa')
        btn_frame.grid(row=3, column=0, columnspan=6, pady=15)

        btn_asignar = tk.Button(btn_frame, text="Asignar", bg='#28a745', fg='white',
                                font=("Arial", 10, "bold"), padx=20, pady=5, command=self.asignar_profesor)
        btn_asignar.pack(side=tk.LEFT, padx=10)

        btn_cancelar = tk.Button(btn_frame, text="Cancelar", bg='#dc3545', fg='white',
                                 font=("Arial", 10), padx=20, pady=5, command=self.clear_form)
        btn_cancelar.pack(side=tk.LEFT, padx=10)

    def load_data(self):
        for row in obtener_profesores():
            self.profesores_tree.insert('', tk.END, values=row)
        for row in obtener_cursos():
            self.cursos_tree.insert('', tk.END, values=row)
        for row in obtener_ciclos_programados():
            self.ciclos_tree.insert('', tk.END, values=row)

    def asignar_profesor(self):
        try:
            id_profesor = int(self.id_profesor_entry.get())
            id_curso = int(self.id_curso_entry.get())
            id_ciclo = int(self.id_ciclo_entry.get())
            hora_inicio = self.hora_inicio_var.get()
            hora_fin = self.hora_fin_var.get()
            dia = self.dia_var.get()

            if not validar_id_profesor(id_profesor):
                raise ValueError("ID de profesor no válido")
            if not validar_id_curso(id_curso):
                raise ValueError("ID de curso no válido")
            if not validar_id_ciclo(id_ciclo):
                raise ValueError("ID de ciclo no válido")

            asignar_profesor(id_profesor, id_curso, id_ciclo, hora_inicio, hora_fin, dia)

            messagebox.showinfo("Éxito", "Profesor asignado correctamente.")
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.id_profesor_entry.delete(0, tk.END)
        self.id_curso_entry.delete(0, tk.END)
        self.id_ciclo_entry.delete(0, tk.END)
        self.hora_inicio_combo.set("08:00")
        self.hora_fin_combo.set("10:00")
        self.dia_var.set("lunes")

    def go_to_main_menu(self):
        if messagebox.askyesno("Confirmar", "¿Desea regresar al menú principal?"):
            self.destroy()
            self.master.deiconify()

def main():
    root = tk.Tk()
    app = AsignarProfesorCiclo()
    root.mainloop()

if __name__ == "__main__":
    main()
