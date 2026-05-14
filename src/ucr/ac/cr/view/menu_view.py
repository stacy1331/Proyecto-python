import tkinter as tk
from tkinter import messagebox


class MenuView:
    def __init__(self, root, login_controller, on_logout=None, on_exit=None):
        self.root = root
        self.login_controller = login_controller
        self.on_logout = on_logout
        self.on_exit = on_exit
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self._build()

    def _build(self):
        archivo_menu = tk.Menu(self.menu, tearoff=0)
        archivo_menu.add_command(label="Cerrar sesión", command=self._cerrar_sesion)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self._salir)

        ayuda_menu = tk.Menu(self.menu, tearoff=0)
        ayuda_menu.add_command(label="Acerca de", command=self._acerca_de)

        self.menu.add_cascade(label="Archivo", menu=archivo_menu)
        self.menu.add_cascade(label="Ayuda", menu=ayuda_menu)

    def _cerrar_sesion(self):
        if not messagebox.askyesno("Cerrar sesión", "¿Desea cerrar la sesión actual?"):
            return

        self.login_controller.cerrar_sesion()

        if self.on_logout is not None:
            self.on_logout()

    def _salir(self):
        if not messagebox.askyesno("Salir", "¿Desea salir del sistema?"):
            return

        if self.on_exit is not None:
            self.on_exit()
        else:
            self.root.destroy()

    def _acerca_de(self):
        messagebox.showinfo(
            "Acerca de",
            "Sistema de Gestión de Avisos Ciudadanos sobre Daños Públicos."
        )