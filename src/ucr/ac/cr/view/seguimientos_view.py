import tkinter as tk
from tkinter import messagebox, ttk


class SeguimientosView(tk.Frame):
    def __init__(self, parent, seguimiento_controller, aviso_controller=None):
        super().__init__(parent)
        self.seguimiento_controller = seguimiento_controller
        self.aviso_controller = aviso_controller
        self._build()
        self._cargar_seguimientos()

    def _build(self):
        form = ttk.LabelFrame(self, text="Registro de seguimientos", padding=12)
        form.pack(fill="x", padx=12, pady=12)

        labels = ["Código seguimiento", "Código aviso", "Estado", "Observación", "Fecha actualización", "Responsable"]
        for i, text in enumerate(labels):
            ttk.Label(form, text=text + ":").grid(row=i, column=0, sticky="e", padx=6, pady=5)

        self.entry_codigo_seguimiento = ttk.Entry(form, width=35)
        self.entry_codigo_aviso = ttk.Entry(form, width=35)
        self.combo_estado = ttk.Combobox(form, values=["Pendiente", "En proceso", "Resuelto"], state="readonly", width=32)
        self.combo_estado.set("Pendiente")
        self.entry_observacion = ttk.Entry(form, width=35)
        self.entry_fecha = ttk.Entry(form, width=35)
        self.entry_responsable = ttk.Entry(form, width=35)

        self.entry_codigo_seguimiento.grid(row=0, column=1, padx=6, pady=5)
        self.entry_codigo_aviso.grid(row=1, column=1, padx=6, pady=5)
        self.combo_estado.grid(row=2, column=1, padx=6, pady=5)
        self.entry_observacion.grid(row=3, column=1, padx=6, pady=5)
        self.entry_fecha.grid(row=4, column=1, padx=6, pady=5)
        self.entry_responsable.grid(row=5, column=1, padx=6, pady=5)

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=0, column=2, rowspan=6, padx=20, pady=5, sticky="ns")

        ttk.Button(btn_frame, text="Registrar", command=self._registrar_seguimiento, width=20).pack(pady=3)
        ttk.Button(btn_frame, text="Buscar por código", command=self._buscar_por_codigo, width=20).pack(pady=3)
        ttk.Button(btn_frame, text="Buscar por aviso", command=self._buscar_por_aviso, width=20).pack(pady=3)
        ttk.Button(btn_frame, text="Listar todos", command=self._cargar_seguimientos, width=20).pack(pady=3)
        ttk.Button(btn_frame, text="Limpiar", command=self._limpiar_formulario, width=20).pack(pady=3)

        table_frame = ttk.LabelFrame(self, text="Listado de seguimientos", padding=12)
        table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        columns = ("codigo_seguimiento", "codigo_aviso", "estado", "observacion", "fecha", "responsable")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        headers = {
            "codigo_seguimiento": "Código seguimiento",
            "codigo_aviso": "Código aviso",
            "estado": "Estado",
            "observacion": "Observación",
            "fecha": "Fecha actualización",
            "responsable": "Responsable"
        }
        widths = {
            "codigo_seguimiento": 140,
            "codigo_aviso": 120,
            "estado": 120,
            "observacion": 280,
            "fecha": 150,
            "responsable": 180
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

    def _limpiar_formulario(self):
        for entry in (
            self.entry_codigo_seguimiento,
            self.entry_codigo_aviso,
            self.entry_observacion,
            self.entry_fecha,
            self.entry_responsable,
        ):
            entry.delete(0, tk.END)
        self.combo_estado.set("Pendiente")
        self.entry_codigo_seguimiento.focus_set()

    def _registrar_seguimiento(self):
        try:
            self.seguimiento_controller.registrar_seguimiento(
                self.entry_codigo_seguimiento.get().strip(),
                self.entry_codigo_aviso.get().strip(),
                self.combo_estado.get().strip(),
                self.entry_observacion.get().strip(),
                self.entry_fecha.get().strip(),
                self.entry_responsable.get().strip()
            )
            messagebox.showinfo("Éxito", "Seguimiento registrado correctamente.")
            self._cargar_seguimientos()
            self._limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _buscar_por_codigo(self):
        try:
            seguimiento = self.seguimiento_controller.buscar_seguimiento_por_codigo(
                self.entry_codigo_seguimiento.get().strip()
            )
            self._cargar_seguimiento_en_formulario(seguimiento)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _buscar_por_aviso(self):
        try:
            codigo_aviso = self.entry_codigo_aviso.get().strip()
            seguimientos = self.seguimiento_controller.obtener_seguimientos_por_aviso(codigo_aviso)
            self._cargar_en_tabla(seguimientos)

            if not seguimientos:
                messagebox.showinfo("Información", "No existen seguimientos para ese aviso.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _cargar_seguimiento_en_formulario(self, seguimiento):
        self.entry_codigo_seguimiento.delete(0, tk.END)
        self.entry_codigo_seguimiento.insert(0, seguimiento.codigo_seguimiento)

        self.entry_codigo_aviso.delete(0, tk.END)
        self.entry_codigo_aviso.insert(0, seguimiento.codigo_aviso)

        self.combo_estado.set(seguimiento.estado)

        self.entry_observacion.delete(0, tk.END)
        self.entry_observacion.insert(0, seguimiento.observacion)

        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, seguimiento.fecha_actualizacion)

        self.entry_responsable.delete(0, tk.END)
        self.entry_responsable.insert(0, seguimiento.responsable)

    def _cargar_seguimientos(self):
        try:
            seguimientos = self.seguimiento_controller.obtener_todos_los_seguimientos()
            self._cargar_en_tabla(seguimientos)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _cargar_en_tabla(self, seguimientos):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for seguimiento in seguimientos:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    seguimiento.codigo_seguimiento,
                    seguimiento.codigo_aviso,
                    seguimiento.estado,
                    seguimiento.observacion,
                    seguimiento.fecha_actualizacion,
                    seguimiento.responsable
                )
            )

    def _on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        if not values:
            return

        self.entry_codigo_seguimiento.delete(0, tk.END)
        self.entry_codigo_seguimiento.insert(0, values[0])
        self.entry_codigo_aviso.delete(0, tk.END)
        self.entry_codigo_aviso.insert(0, values[1])
        self.combo_estado.set(values[2])
        self.entry_observacion.delete(0, tk.END)
        self.entry_observacion.insert(0, values[3])
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, values[4])
        self.entry_responsable.delete(0, tk.END)
        self.entry_responsable.insert(0, values[5])