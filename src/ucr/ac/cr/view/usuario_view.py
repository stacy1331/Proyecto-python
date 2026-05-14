import tkinter as tk
from tkinter import messagebox, ttk


class UsuarioView(tk.Frame):
    def __init__(self, parent, usuario_controller):
        super().__init__(parent)
        self.usuario_controller = usuario_controller
        self._build()
        self._cargar_usuarios()

    def _build(self):
        form = ttk.LabelFrame(self, text="Registro de usuarios", padding=12)
        form.pack(fill="x", padx=12, pady=12)

        labels = ["Cédula", "Nombre", "Correo", "Contraseña", "Rol"]
        for i, text in enumerate(labels):
            ttk.Label(form, text=text + ":").grid(row=i, column=0, sticky="e", padx=6, pady=6)

        self.entry_cedula = ttk.Entry(form, width=35)
        self.entry_nombre = ttk.Entry(form, width=35)
        self.entry_correo = ttk.Entry(form, width=35)
        self.entry_contrasena = ttk.Entry(form, width=35, show="*")
        self.combo_rol = ttk.Combobox(form, values=["Ciudadano", "Administrador"], state="readonly", width=32)
        self.combo_rol.set("Ciudadano")

        self.entry_cedula.grid(row=0, column=1, padx=6, pady=6)
        self.entry_nombre.grid(row=1, column=1, padx=6, pady=6)
        self.entry_correo.grid(row=2, column=1, padx=6, pady=6)
        self.entry_contrasena.grid(row=3, column=1, padx=6, pady=6)
        self.combo_rol.grid(row=4, column=1, padx=6, pady=6)

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=0, column=2, rowspan=5, padx=20, pady=6, sticky="ns")

        ttk.Button(btn_frame, text="Registrar", command=self._registrar_usuario, width=18).pack(pady=4)
        ttk.Button(btn_frame, text="Buscar por cédula", command=self._buscar_usuario, width=18).pack(pady=4)
        ttk.Button(btn_frame, text="Limpiar", command=self._limpiar_formulario, width=18).pack(pady=4)
        ttk.Button(btn_frame, text="Actualizar listado", command=self._cargar_usuarios, width=18).pack(pady=4)

        self.entry_cedula.bind("<Return>", lambda event: self._buscar_usuario())

        table_frame = ttk.LabelFrame(self, text="Listado de usuarios", padding=12)
        table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        columns = ("cedula", "nombre", "correo", "rol")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        headings = {
            "cedula": "Cédula",
            "nombre": "Nombre",
            "correo": "Correo",
            "rol": "Rol"
        }
        widths = {"cedula": 120, "nombre": 220, "correo": 260, "rol": 140}

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _limpiar_formulario(self):
        for entry in (self.entry_cedula, self.entry_nombre, self.entry_correo, self.entry_contrasena):
            entry.delete(0, tk.END)
        self.combo_rol.set("Ciudadano")
        self.entry_cedula.focus_set()

    def _registrar_usuario(self):
        try:
            self.usuario_controller.registrar_usuario(
                self.entry_cedula.get().strip(),
                self.entry_nombre.get().strip(),
                self.entry_correo.get().strip(),
                self.entry_contrasena.get().strip(),
                self.combo_rol.get().strip()
            )
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self._limpiar_formulario()
            self._cargar_usuarios()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _buscar_usuario(self):
        try:
            cedula = self.entry_cedula.get().strip()
            usuario = self.usuario_controller.buscar_usuario_por_cedula(cedula)

            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, usuario.nombre)

            self.entry_correo.delete(0, tk.END)
            self.entry_correo.insert(0, usuario.correo)

            self.entry_contrasena.delete(0, tk.END)
            self.entry_contrasena.insert(0, usuario.contrasena)

            self.combo_rol.set(usuario.rol)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _cargar_usuarios(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            usuarios = self.usuario_controller.obtener_todos_los_usuarios()
            for usuario in usuarios:
                self.tree.insert("", tk.END, values=(usuario.cedula, usuario.nombre, usuario.correo, usuario.rol))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        if not values:
            return

        self.entry_cedula.delete(0, tk.END)
        self.entry_cedula.insert(0, values[0])

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, values[1])

        self.entry_correo.delete(0, tk.END)
        self.entry_correo.insert(0, values[2])

        self.combo_rol.set(values[3])