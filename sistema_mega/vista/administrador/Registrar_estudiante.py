import tkinter as tk
from tkinter import ttk, messagebox
from sistema_mega.modelo.registrar_estudiante import (
    obtener_sedes, obtener_ciclos_por_sede, obtener_grupos_por_ciclo,
    registrar_usuario, registrar_estudiante, registrar_inscripcion, registrar_pago, registrar_estudiante_con_sp
)

class VistaRegistroEstudiante(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Registro de Estudiante")
        self.geometry("+200+100")

        self.sedes = obtener_sedes()
        self.ciclos = []
        self.grupos = []

        self.campos = {}
        self.contrasenia_visible = False
        self.crear_formulario()

    def crear_formulario(self):
        frame = ttk.Frame(self, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        estilo = {'padx': 8, 'pady': 6, 'sticky': 'w'}

        self.agregar_entry(frame, "Nombres", 0, 0, estilo)
        self.agregar_entry(frame, "Apellido Paterno", 0, 1, estilo)
        self.agregar_entry(frame, "Apellido Materno", 0, 2, estilo)

        ttk.Label(frame, text="Tipo de Documento").grid(row=1, column=0, **estilo)
        self.cmb_tipo_doc = ttk.Combobox(frame, values=["dni", "pasaporte"], state="readonly", width=20)
        self.cmb_tipo_doc.grid(row=1, column=1, **estilo)
        self.cmb_tipo_doc.current(0)

        ttk.Label(frame, text="Número de Documento").grid(row=1, column=2, **estilo)
        self.entry_dni = ttk.Entry(frame, width=25)
        self.entry_dni.grid(row=1, column=3, sticky="w", padx=(8, 0))
        self.campos["Número de Documento"] = self.entry_dni

        self.btn_generar = ttk.Button(frame, text="Generar", width=10, command=self.autocompletar_usuario)
        self.btn_generar.grid(row=1, column=4, sticky="w")

        ttk.Label(frame, text="Área Académica").grid(row=2, column=0, **estilo)
        self.cmb_area = ttk.Combobox(frame, values=["a", "b", "c", "d", "e"], state="readonly", width=20)
        self.cmb_area.grid(row=2, column=1, **estilo)
        self.cmb_area.current(0)

        ttk.Label(frame, text="Nombre de Usuario").grid(row=2, column=2, **estilo)
        self.entry_usuario = ttk.Entry(frame, state="readonly", width=30)
        self.entry_usuario.grid(row=2, column=3, columnspan=2, sticky="ew")

        ttk.Label(frame, text="Correo Institucional").grid(row=3, column=0, **estilo)
        self.entry_correo = ttk.Entry(frame, state="readonly", width=30)
        self.entry_correo.grid(row=3, column=1, columnspan=2, sticky="ew")

        ttk.Label(frame, text="Contraseña").grid(row=3, column=3, **estilo)
        contra_frame = ttk.Frame(frame)
        contra_frame.grid(row=3, column=4, sticky="ew", padx=8)

        self.entry_contra = ttk.Entry(contra_frame, show="*", width=25)
        self.entry_contra.pack(side="left", fill="x", expand=True)

        self.btn_toggle_contra = ttk.Button(
            contra_frame, text="👁 Mostrar", width=10, command=self.toggle_contrasenia
        )
        self.btn_toggle_contra.pack(side="left", padx=4)

        ttk.Label(frame, text="Sede").grid(row=4, column=0, **estilo)
        self.cmb_sede = ttk.Combobox(frame, values=[s[1] for s in self.sedes], state="readonly", width=30)
        self.cmb_sede.grid(row=4, column=1, columnspan=2, sticky="ew")
        self.cmb_sede.bind("<<ComboboxSelected>>", self.actualizar_ciclos)

        ttk.Label(frame, text="Ciclo Programado").grid(row=4, column=3, **estilo)
        self.cmb_ciclo = ttk.Combobox(frame, state="readonly", width=30)
        self.cmb_ciclo.grid(row=4, column=4, sticky="ew")
        self.cmb_ciclo.bind("<<ComboboxSelected>>", self.actualizar_grupos)

        ttk.Label(frame, text="Grupo").grid(row=5, column=0, **estilo)
        self.cmb_grupo = ttk.Combobox(frame, state="readonly", width=30)
        self.cmb_grupo.grid(row=5, column=1, sticky="ew")

        self.lbl_vacantes = ttk.Label(frame, text="Vacantes disponibles: -", font=("Segoe UI", 10, "italic"))
        self.lbl_vacantes.grid(row=5, column=2, columnspan=3, sticky="w", padx=8)

        self.agregar_entry(frame, "Pago realizado (S/.)", 6, 0, estilo)

        ttk.Button(frame, text="Guardar", command=self.registrar, width=20).grid(row=7, column=2, pady=20)
        ttk.Button(frame, text="Cancelar", command=self.quit, width=20).grid(row=7, column=3, pady=20)

        for i in range(5):
            frame.columnconfigure(i, weight=1)

    def agregar_entry(self, parent, label, row, col, estilo):
        ttk.Label(parent, text=label).grid(row=row, column=col*2, **estilo)
        entry = ttk.Entry(parent, width=30)
        entry.grid(row=row, column=col*2+1, **estilo)
        self.campos[label] = entry

    def autocompletar_usuario(self):
        dni = self.campos["Número de Documento"].get().strip()

        self.entry_usuario.config(state="normal")
        self.entry_usuario.delete(0, tk.END)
        self.entry_correo.config(state="normal")
        self.entry_correo.delete(0, tk.END)
        self.entry_contra.delete(0, tk.END)

        if dni:
            self.entry_usuario.insert(0, dni)
            self.entry_correo.insert(0, f"{dni}@acadmega.edu.pe")
            self.entry_contra.insert(0, dni)

        self.entry_usuario.config(state="readonly")
        self.entry_correo.config(state="readonly")

    def toggle_contrasenia(self):
        if self.contrasenia_visible:
            self.entry_contra.config(show="*")
            self.btn_toggle_contra.config(text="Mostrar")
            self.contrasenia_visible = False
        else:
            self.entry_contra.config(show="")
            self.btn_toggle_contra.config(text="Ocultar")
            self.contrasenia_visible = True

    def actualizar_ciclos(self, event=None):
        index = self.cmb_sede.current()
        if index >= 0:
            id_sede = self.sedes[index][0]
            self.ciclos = obtener_ciclos_por_sede(id_sede)
            self.cmb_ciclo['values'] = [c[1] for c in self.ciclos]
            if self.ciclos:
                self.cmb_ciclo.current(0)
                self.actualizar_grupos()

    def actualizar_grupos(self, event=None):
        index = self.cmb_ciclo.current()
        if index >= 0:
            id_ciclo = self.ciclos[index][0]
            self.grupos = obtener_grupos_por_ciclo(id_ciclo)
            self.cmb_grupo['values'] = [g[1] for g in self.grupos]
            if self.grupos:
                self.cmb_grupo.current(0)
                self.lbl_vacantes.config(text=f"Vacantes disponibles: {self.grupos[0][2]}")
            else:
                self.cmb_grupo.set("")
                self.lbl_vacantes.config(text="Vacantes disponibles: -")

    def registrar(self):
        try:
            nombre = self.campos["Nombres"].get().strip()
            ap_paterno = self.campos["Apellido Paterno"].get().strip()
            ap_materno = self.campos["Apellido Materno"].get().strip()
            tipo_doc = self.cmb_tipo_doc.get()
            nro_doc = self.campos["Número de Documento"].get().strip()
            area = self.cmb_area.get()
            usuario = nro_doc
            correo = f"{nro_doc}@acadmega.edu.pe"
            contrasenia = self.entry_contra.get()

            pago_str = self.campos["Pago realizado (S/.)"].get().strip()
            if not pago_str:
                messagebox.showwarning("Dato faltante", "Debe ingresar un monto para el pago.")
                return

            try:
                pago = float(pago_str)
                if pago <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Monto inválido", "El monto debe ser un número positivo.")
                return

            id_ciclo = self.ciclos[self.cmb_ciclo.current()][0]
            id_grupo = self.grupos[self.cmb_grupo.current()][0]

            # ✅ Llamar al procedimiento almacenado
            mensaje = registrar_estudiante_con_sp(
                usuario, correo, contrasenia,
                nombre, ap_paterno, ap_materno,
                tipo_doc, nro_doc, area,
                id_grupo, id_ciclo, pago
            )

            if mensaje:
                messagebox.showinfo("Resultado", mensaje)
            else:
                raise ValueError("No se recibió respuesta del procedimiento.")

        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al registrar:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaRegistroEstudiante(root)
    root.mainloop()
