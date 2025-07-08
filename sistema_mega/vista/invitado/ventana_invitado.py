import tkinter as tk
from tkinter import ttk, messagebox
from sistema_mega.database.conexion_invitado import ejecutar_select

class VentanaInvitado(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Ciclos Disponibles - Academia Mega")
        self.geometry("1000x600")
        self.configure(bg="#f0f8ff")  # Fondo azul claro
        self.master = master

        self._configurar_estilos()
        self._crear_widgets()
        self._cargar_ciclos()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Main.TFrame', background='#f0f8ff')

        style.configure('Ciclo.TFrame',
                        background='#2a5c8f',
                        borderwidth=0,
                        relief='solid',
                        padding=15)

        style.configure('Title.TLabel',
                        font=('Arial', 16, 'bold'),
                        background='#2a5c8f',
                        foreground='white')

        style.configure('Info.TLabel',
                        font=('Arial', 12),
                        background='#2a5c8f',
                        foreground='white')

        style.configure('Header.TLabel',
                        font=('Arial', 20, 'bold'),
                        background='#f0f8ff',
                        foreground='#2a5c8f')

        style.configure('Login.TButton',
                        font=('Arial', 12, 'bold'),
                        background='#2a5c8f',
                        foreground='white',
                        padding=12,
                        borderwidth=0)
        style.map('Login.TButton', background=[('active', '#1a4a7f')])

    def _crear_widgets(self):
        self.main_frame = ttk.Frame(self, style='Main.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=40, pady=40)

        header = ttk.Frame(self.main_frame, style='Main.TFrame')
        header.pack(fill='x', pady=(0, 30))
        ttk.Label(header, text="Nuestros Ciclos Disponibles", style='Header.TLabel').pack()

        # Scrollable canvas
        canvas_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        canvas_frame.pack(fill='both', expand=True)

        canvas = tk.Canvas(canvas_frame, background='#f0f8ff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, style='Main.TFrame')

        self.scrollable_frame.bind(
            '<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        btn_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        btn_frame.pack(fill='x', pady=(30, 0))
        ttk.Button(btn_frame, text="Iniciar Sesión", style='Login.TButton', command=self._ir_a_login).pack(ipadx=30)

    def _cargar_ciclos(self):
        """Carga los ciclos no finalizados desde la base de datos"""
        query = """
        SELECT * FROM vista_ciclos_pendientes;
        """

        try:
            ciclos = ejecutar_select(query)

            if not ciclos:
                ttk.Label(
                    self.scrollable_frame,
                    text="No hay ciclos disponibles actualmente",
                    style='Info.TLabel',
                    background='#f0f8ff',
                    foreground='#2a5c8f'
                ).pack(pady=50)
                return

            for i, ciclo in enumerate(ciclos):
                card = ttk.Frame(self.scrollable_frame, style='Ciclo.TFrame')
                row = i // 3
                col = i % 3
                card.grid(row=row, column=col, padx=20, pady=20, sticky='nsew')

                # Nombre del ciclo
                ttk.Label(
                    card,
                    text=ciclo[0],  # nombre_ciclo
                    style='Title.TLabel'
                ).pack(pady=(0, 15))

                info_frame = ttk.Frame(card, style='Ciclo.TFrame')
                info_frame.pack(fill='x')

                # Modalidad
                ttk.Label(
                    info_frame,
                    text=f"Modalidad: {ciclo[1]}",  # modalidad
                    style='Info.TLabel'
                ).pack(anchor='w', pady=2)

                # Costo
                ttk.Label(
                    info_frame,
                    text=f"Costo: S/. {float(ciclo[2]):.2f}",  # costo
                    style='Info.TLabel'
                ).pack(anchor='w', pady=2)

                # Fechas
                fecha_inicio = ciclo[3].strftime("%d/%m/%Y") if ciclo[3] else "No definida"
                fecha_fin = ciclo[4].strftime("%d/%m/%Y") if ciclo[4] else "No definida"

                ttk.Label(
                    info_frame,
                    text=f"Inicio: {fecha_inicio}",  # fecha_inicio
                    style='Info.TLabel'
                ).pack(anchor='w', pady=2)

                ttk.Label(
                    info_frame,
                    text=f"Fin: {fecha_fin}",  # fecha_fin
                    style='Info.TLabel'
                ).pack(anchor='w', pady=2)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los ciclos: {str(e)}")

    def _ir_a_login(self):
        self.destroy()
        self.master.deiconify()

    def mostrar(self):
        self.mainloop()
