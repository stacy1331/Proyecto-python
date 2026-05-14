import tkinter as tk
from tkinter import ttk


class ReportesView(tk.Frame):
    def __init__(self, parent, reporte_controller):
        super().__init__(parent)
        self.reporte_controller = reporte_controller
        self._build()
        self._actualizar()

    def _build(self):
        resumen = ttk.LabelFrame(self, text="Estadísticas generales", padding=12)
        resumen.pack(fill="x", padx=12, pady=12)

        self.lbl_total = ttk.Label(resumen, text="Total de avisos: 0", font=("Arial", 12, "bold"))
        self.lbl_pendientes = ttk.Label(resumen, text="Pendientes: 0", font=("Arial", 12))
        self.lbl_en_proceso = ttk.Label(resumen, text="En proceso: 0", font=("Arial", 12))
        self.lbl_resueltos = ttk.Label(resumen, text="Resueltos: 0", font=("Arial", 12))

        self.lbl_total.grid(row=0, column=0, padx=10, pady=6, sticky="w")
        self.lbl_pendientes.grid(row=1, column=0, padx=10, pady=6, sticky="w")
        self.lbl_en_proceso.grid(row=2, column=0, padx=10, pady=6, sticky="w")
        self.lbl_resueltos.grid(row=3, column=0, padx=10, pady=6, sticky="w")

        ttk.Button(resumen, text="Actualizar reportes", command=self._actualizar).grid(
            row=0, column=1, rowspan=4, padx=20, pady=10, sticky="ns"
        )

        tipos_frame = ttk.LabelFrame(self, text="Conteo por tipo de daño", padding=12)
        tipos_frame.pack(fill="x", padx=12, pady=(0, 12))

        self.tree_tipos = ttk.Treeview(tipos_frame, columns=("tipo", "cantidad"), show="headings", height=6)
        self.tree_tipos.heading("tipo", text="Tipo de daño")
        self.tree_tipos.heading("cantidad", text="Cantidad")
        self.tree_tipos.column("tipo", width=360, anchor="center")
        self.tree_tipos.column("cantidad", width=120, anchor="center")

        scrollbar_tipos = ttk.Scrollbar(tipos_frame, orient="vertical", command=self.tree_tipos.yview)
        self.tree_tipos.configure(yscrollcommand=scrollbar_tipos.set)

        self.tree_tipos.grid(row=0, column=0, sticky="nsew")
        scrollbar_tipos.grid(row=0, column=1, sticky="ns")

        tipos_frame.grid_rowconfigure(0, weight=1)
        tipos_frame.grid_columnconfigure(0, weight=1)

        general_frame = ttk.LabelFrame(self, text="Listado general de avisos", padding=12)
        general_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        columns = ("codigo", "cedula", "tipo", "descripcion", "ubicacion", "fecha", "estado")
        self.tree = ttk.Treeview(general_frame, columns=columns, show="headings", height=10)

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

        scrollbar_y = ttk.Scrollbar(general_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(general_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        general_frame.grid_rowconfigure(0, weight=1)
        general_frame.grid_columnconfigure(0, weight=1)

    def _actualizar(self):
        estadisticas = self.reporte_controller.obtener_estadisticas_generales()

        self.lbl_total.config(text=f"Total de avisos: {estadisticas.get('total', 0)}")
        self.lbl_pendientes.config(text=f"Pendientes: {estadisticas.get('pendientes', 0)}")
        self.lbl_en_proceso.config(text=f"En proceso: {estadisticas.get('en_proceso', 0)}")
        self.lbl_resueltos.config(text=f"Resueltos: {estadisticas.get('resueltos', 0)}")

        for item in self.tree_tipos.get_children():
            self.tree_tipos.delete(item)

        conteo_tipos = self.reporte_controller.contar_avisos_por_tipo()
        for tipo, cantidad in sorted(conteo_tipos.items()):
            self.tree_tipos.insert("", tk.END, values=(tipo, cantidad))

        for item in self.tree.get_children():
            self.tree.delete(item)

        avisos = self.reporte_controller.obtener_listado_general_avisos()
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