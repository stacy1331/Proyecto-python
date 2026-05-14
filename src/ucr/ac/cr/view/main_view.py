import tkinter as tk
from tkinter import ttk

from src.ucr.ac.cr.view.avisos_view import AvisosView
from src.ucr.ac.cr.view.menu_view import MenuView
from src.ucr.ac.cr.view.reportes_view import ReportesView
from src.ucr.ac.cr.view.seguimientos_view import SeguimientosView
from src.ucr.ac.cr.view.usuario_view import UsuarioView


class MainView(tk.Frame):
    def __init__(self, root, main_controller, on_logout=None):
        super().__init__(root)
        self.root = root
        self.main_controller = main_controller
        self.on_logout = on_logout
        self._build()

    def _build(self):
        self.pack(fill="both", expand=True)

        self.root.title("Sistema de Gestión de Avisos Ciudadanos")
        self.root.geometry("1200x780")
        self.root.minsize(1100, 720)

        MenuView(
            self.root,
            self.main_controller.login_controller,
            on_logout=self._logout,
            on_exit=self.root.destroy
        )

        encabezado = ttk.Frame(self, padding=(18, 16))
        encabezado.pack(fill="x")

        ttk.Label(
            encabezado,
            text="Sistema de Gestión de Avisos Ciudadanos sobre Daños Públicos",
            font=("Arial", 18, "bold")
        ).pack(anchor="w")

        usuario_actual = self.main_controller.login_controller.usuario_actual
        if usuario_actual is not None:
            ttk.Label(
                encabezado,
                text=f"Usuario activo: {usuario_actual.nombre} ({usuario_actual.rol})",
                font=("Arial", 11)
            ).pack(anchor="w", pady=(6, 0))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=12, pady=12)

        if self.main_controller.login_controller.es_administrador():
            usuario_view = UsuarioView(notebook, self.main_controller.usuario_controller)
            aviso_view = AvisosView(
                notebook,
                self.main_controller.aviso_controller,
                self.main_controller.login_controller
            )
            seguimiento_view = SeguimientosView(
                notebook,
                self.main_controller.seguimiento_controller,
                self.main_controller.aviso_controller
            )
            reporte_view = ReportesView(notebook, self.main_controller.reporte_controller)

            notebook.add(usuario_view, text="Usuarios")
            notebook.add(aviso_view, text="Avisos")
            notebook.add(seguimiento_view, text="Seguimientos")
            notebook.add(reporte_view, text="Reportes")

        else:
            aviso_view = AvisosView(
                notebook,
                self.main_controller.aviso_controller,
                self.main_controller.login_controller
            )
            notebook.add(aviso_view, text="Avisos")

        notebook.bind("<<NotebookTabChanged>>", lambda event: self._refrescar_tab(notebook))

    def _refrescar_tab(self, notebook):
        try:
            current = notebook.nametowidget(notebook.select())
            if hasattr(current, "_actualizar"):
                current._actualizar()
            elif hasattr(current, "_cargar_usuarios"):
                current._cargar_usuarios()
            elif hasattr(current, "_cargar_avisos"):
                current._cargar_avisos()
            elif hasattr(current, "_cargar_seguimientos"):
                current._cargar_seguimientos()
        except Exception:
            pass

    def _logout(self):
        self.destroy()
        if self.on_logout is not None:
            self.on_logout()