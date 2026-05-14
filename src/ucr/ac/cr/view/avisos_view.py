import tkinter as tk
from tkinter import messagebox, ttk


class AvisosView(tk.Frame):
    def __init__(self, parent, aviso_controller, login_controller=None):
        super().__init__(parent)
        self.aviso_controller = aviso_controller
        self.login_controller = login_controller
        self._build()
        self._cargar_avisos()

    def _build(self):
        form = ttk.LabelFrame(self, text="Registro de avisos", padding=12)
        form.pack(fill="x", padx=12, pady=12)

        labels = ["Código", "Cédula usuario", "Tipo de daño", "Descripción", "Ubicación", "Fecha", "Estado"]
        for i, text in enumerate(labels):
            ttk.Label(form, text=text + ":").grid(row=i, column=0, sticky="e", padx=6, pady=5)

        self.entry_codigo = ttk.Entry(form, width=35)
        self.entry_cedula = ttk.Entry(form, width=35)
        self.combo_tipo_dano = ttk.Combobox(
            form,
            values=[
                "Calle dañada",
                "Fuga de agua",
                "Alumbrado público dañado",
                "Basura acumulada",
                "Acera dañada",
                "Alcantarilla dañada",
                "Señal de tránsito dañada",
                "Otro"
            ],
            state="readonly",
            width=32
        )
        self.combo_tipo_dano.set("Calle dañada")
        self.entry_descripcion = ttk.Entry(form, width=35)
        self.entry_ubicacion = ttk.Entry(form, width=35)
        self.entry_fecha = ttk.Entry(form, width=35)
        self.combo_estado = ttk.Combobox(form, values=["Pendiente", "En proceso", "Resuelto"], state="readonly", width=32)
        self.combo_estado.set("Pendiente")

        self.entry_codigo.grid(row=0, column=1, padx=6, pady=5)
        self.entry_cedula.grid(row=1, column=1, padx=6, pady=5)
        self.combo_tipo_dano.grid(row=2, column=1, padx=6, pady=5)
        self.entry_descripcion.grid(row=3, column=1, padx=6, pady=5)
        self.entry_ubicacion.grid(row=4, column=1, padx=6, pady=5)
        self.entry_fecha.grid(row=5, column=1, padx=6, pady=5)
        self.combo_estado.grid(row=6, column=1, padx=6, pady=5)

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=0, column=2, rowspan=7, padx=20, pady=5, sticky="ns")

        ttk.Button(btn_frame, text="Registrar", command=self._registrar_aviso, width=20).pack(pady=3)
        ttk.Button(btn_frame, text="Buscar por código", command=self._buscar_por_codigo, width=20).pack(pady=3)
        ttk.Button(btn_frame, text="Buscar por cédula", command=self._buscar_por_usuario, width=20).pack(pady=3)
        ttk.Button(btn_frame, text="Actualizar estado", command=self._actualizar_estado, width=20).pack(pady=3)
        ttk.Button(btn_frame, text="Listar todos", command=self._cargar_avisos, width=20).pack(pady=3)
        ttk.Button(btn_frame, text="Limpiar", command=self._limpiar_formulario, width=20).pack(pady=3)

        table_frame = ttk.LabelFrame(self, text="Listado de avisos", padding=12)
        table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        columns = ("codigo", "cedula", "tipo", "descripcion", "ubicacion", "fecha", "estado")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        headers = {
            "codigo": "Código",
            "cedula": "Cédula",
            "tipo": "Tipo de daño",
            "descripcion": "Descripción",
            "ubicacion": "Ubicación",
            "fecha": "Fecha",
            "estado": "Estado"
        }
        widths = {
            "codigo": 100,
            "cedula": 120,
            "tipo": 200,
            "descripcion": 240,
            "ubicacion": 180,
            "fecha": 120,
            "estado": 120
        }

        for col in columns:
            self.tree.heading(col, text=headers[col])
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

        if self.login_controller is not None and self.login_controller.usuario_actual is not None:
            if self.login_controller.es_ciudadano():
                self.entry_cedula.delete(0, tk.END)
                self.entry_cedula.insert(0, self.login_controller.usuario_actual.cedula)
                self.entry_cedula.config(state="readonly")

    def _limpiar_formulario(self):
        self.entry_codigo.delete(0, tk.END)

        if self.entry_cedula.cget("state") != "readonly":
            self.entry_cedula.delete(0, tk.END)

        self.combo_tipo_dano.set("Calle dañada")
        self.entry_descripcion.delete(0, tk.END)
        self.entry_ubicacion.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.combo_estado.set("Pendiente")
        self.entry_codigo.focus_set()

    def _registrar_aviso(self):
        try:
            self.aviso_controller.registrar_aviso(
                self.entry_codigo.get().strip(),
                self.entry_cedula.get().strip(),
                self.combo_tipo_dano.get().strip(),
                self.entry_descripcion.get().strip(),
                self.entry_ubicacion.get().strip(),
                self.entry_fecha.get().strip()
            )
            messagebox.showinfo("Éxito", "Aviso registrado correctamente.")
            self._cargar_avisos()
            self._limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _buscar_por_codigo(self):
        try:
            aviso = self.aviso_controller.buscar_aviso_por_codigo(self.entry_codigo.get().strip())
            self._cargar_aviso_en_formulario(aviso)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _buscar_por_usuario(self):
        try:
            cedula = self.entry_cedula.get().strip()
            avisos = self.aviso_controller.obtener_avisos_por_usuario(cedula)
            self._cargar_en_tabla(avisos)

            if not avisos:
                messagebox.showinfo("Información", "No existen avisos para esa cédula.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _actualizar_estado(self):
        try:
            codigo = self.entry_codigo.get().strip()
            estado = self.combo_estado.get().strip()
            self.aviso_controller.actualizar_estado_aviso(codigo, estado)
            messagebox.showinfo("Éxito", "Estado actualizado correctamente.")
            self._cargar_avisos()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _cargar_aviso_en_formulario(self, aviso):
        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, aviso.codigo)

        if self.entry_cedula.cget("state") != "readonly":
            self.entry_cedula.delete(0, tk.END)
            self.entry_cedula.insert(0, aviso.cedula_usuario)

        self.combo_tipo_dano.set(aviso.tipo_dano)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_descripcion.insert(0, aviso.descripcion)
        self.entry_ubicacion.delete(0, tk.END)
        self.entry_ubicacion.insert(0, aviso.ubicacion)
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, aviso.fecha)
        self.combo_estado.set(aviso.estado)

    def _cargar_avisos(self):
        try:
            avisos = self.aviso_controller.obtener_todos_los_avisos()
            self._cargar_en_tabla(avisos)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _cargar_en_tabla(self, avisos):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for aviso in avisos:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    aviso.codigo,
                    aviso.cedula_usuario,
                    aviso.tipo_dano,
                    aviso.descripcion,
                    aviso.ubicacion,
                    aviso.fecha,
                    aviso.estado
                )
            )

    def _on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        if not values:
            return

        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, values[0])

        if self.entry_cedula.cget("state") != "readonly":
            self.entry_cedula.delete(0, tk.END)
            self.entry_cedula.insert(0, values[1])

        self.combo_tipo_dano.set(values[2])
        self.entry_descripcion.delete(0, tk.END)
        self.entry_descripcion.insert(0, values[3])
        self.entry_ubicacion.delete(0, tk.END)
        self.entry_ubicacion.insert(0, values[4])
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, values[5])
        self.combo_estado.set(values[6])