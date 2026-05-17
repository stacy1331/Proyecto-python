import tkinter as tk
from tkinter import ttk


class ReportesView(tk.Frame):
    def __init__(self, parent, reporte_controller):
        super().__init__(parent)
        self.reporte_controller = reporte_controller
        self._build()
        self._actualizar()

    def _build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        resumen = ttk.LabelFrame(self, text="Estadísticas generales", padding=10)
        resumen.grid(row=0, column=0, padx=10, pady=8, sticky="ew")

        resumen.columnconfigure(0, weight=1)
        resumen.columnconfigure(1, weight=1)

        self.lbl_total = ttk.Label(resumen, text="Total de avisos: 0", font=("Arial", 11, "bold"))
        self.lbl_pendientes = ttk.Label(resumen, text="Pendientes: 0", font=("Arial", 10))
        self.lbl_en_proceso = ttk.Label(resumen, text="En proceso: 0", font=("Arial", 10))
        self.lbl_resueltos = ttk.Label(resumen, text="Resueltos: 0", font=("Arial", 10))

        self.lbl_total.grid(row=0, column=0, padx=10, pady=3, sticky="w")
        self.lbl_pendientes.grid(row=1, column=0, padx=10, pady=3, sticky="w")
        self.lbl_en_proceso.grid(row=2, column=0, padx=10, pady=3, sticky="w")
        self.lbl_resueltos.grid(row=3, column=0, padx=10, pady=3, sticky="w")

        ttk.Button(
            resumen,
            text="Actualizar reportes",
            command=self._actualizar
        ).grid(row=0, column=1, rowspan=4, padx=10, pady=5, sticky="ns")

        tipos_frame = ttk.LabelFrame(self, text="Conteo por tipo de daño", padding=10)
        tipos_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        tipos_frame.columnconfigure(0, weight=1)

        self.tree_tipos = ttk.Treeview(
            tipos_frame,
            columns=("tipo", "cantidad"),
            show="headings",
            height=4
        )

        self.tree_tipos.heading("tipo", text="Tipo de daño")
        self.tree_tipos.heading("cantidad", text="Cantidad")

        self.tree_tipos.column("tipo", width=300, anchor="center")
        self.tree_tipos.column("cantidad", width=120, anchor="center")

        self.tree_tipos.grid(row=0, column=0, sticky="ew")

        general_frame = ttk.LabelFrame(self, text="Listado general de avisos", padding=10)
        general_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        general_frame.columnconfigure(0, weight=1)
        general_frame.rowconfigure(0, weight=1)

        columns = ("codigo", "cedula", "tipo", "descripcion", "ubicacion", "fecha", "estado")

        self.tree = ttk.Treeview(
            general_frame,
            columns=columns,
            show="headings",
            height=6
        )

        self.tree.heading("codigo", text="Código")
        self.tree.heading("cedula", text="Cédula")
        self.tree.heading("tipo", text="Tipo de daño")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("ubicacion", text="Ubicación")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("estado", text="Estado")

        self.tree.column("codigo", width=80, anchor="center")
        self.tree.column("cedula", width=100, anchor="center")
        self.tree.column("tipo", width=130, anchor="center")
        self.tree.column("descripcion", width=220, anchor="center")
        self.tree.column("ubicacion", width=150, anchor="center")
        self.tree.column("fecha", width=100, anchor="center")
        self.tree.column("estado", width=100, anchor="center")

        scrollbar_y = ttk.Scrollbar(general_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(general_frame, orient="horizontal", command=self.tree.xview)

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

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