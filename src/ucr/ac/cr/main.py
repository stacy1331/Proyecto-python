import json
import os
import tkinter as tk
from tkinter import messagebox

# Importa los controladores, repositorios, servicios y vistas necesarios.
from src.ucr.ac.cr.controller.aviso_controller import AvisoController
from src.ucr.ac.cr.controller.login_controller import LoginController
from src.ucr.ac.cr.controller.main_controller import MainController
from src.ucr.ac.cr.controller.reporte_controller import ReporteController
from src.ucr.ac.cr.controller.seguimiento_controller import SeguimientoController
from src.ucr.ac.cr.controller.usuario_controller import UsuarioController

from src.ucr.ac.cr.repository.aviso_repository import AvisoRepository
from src.ucr.ac.cr.repository.segimiento_repository import SeguimientoRepository
from src.ucr.ac.cr.repository.usuario_repository import UsuarioRepository

from src.ucr.ac.cr.service.auth_service import AuthService
from src.ucr.ac.cr.service.aviso_service import AvisoService
from src.ucr.ac.cr.service.reporte_service import ReporteService
from src.ucr.ac.cr.service.seguimiento_service import SeguimientoService
from src.ucr.ac.cr.service.usuario_service import UsuarioService

from src.ucr.ac.cr.view.login_view import LoginView
from src.ucr.ac.cr.view.main_view import MainView

# Prepara los archivos JSON necesarios para que el sistema pueda guardar datos.
def preparar_archivos_json():
    os.makedirs("data", exist_ok=True)

    archivos = [
        "data/usuarios.json",
        "data/avisos.json",
        "data/seguimientos.json"
    ]

    for archivo in archivos:
        try:
            if not os.path.exists(archivo):
                raise FileNotFoundError

            with open(archivo, "r", encoding="utf-8") as file:
                contenido = file.read().strip()

            if contenido == "":
                raise ValueError

            json.loads(contenido)

        except:
            # Si el archivo no existe, está vacío o da error, lo inicializa como lista vacía.
            with open(archivo, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)


class App:
    def __init__(self):
        preparar_archivos_json()
        # Configuración principal de la ventana.
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Avisos Ciudadanos")
        self.root.geometry("900x600")
        self.root.minsize(850, 550)

        self.main_controller = self._crear_controladores()
        self._crear_usuario_administrador_inicial()
        self.mostrar_login()

    def _crear_controladores(self):
        # Crea repositorios, servicios y controladores, conectando las capas del sistema.
        usuario_repository = UsuarioRepository()
        aviso_repository = AvisoRepository()
        seguimiento_repository = SeguimientoRepository()

        usuario_service = UsuarioService(usuario_repository)
        auth_service = AuthService(usuario_repository)
        aviso_service = AvisoService(aviso_repository, usuario_repository)
        seguimiento_service = SeguimientoService(seguimiento_repository, aviso_repository)
        reporte_service = ReporteService(aviso_repository)

        usuario_controller = UsuarioController(usuario_service)
        login_controller = LoginController(auth_service)
        aviso_controller = AvisoController(aviso_service)
        seguimiento_controller = SeguimientoController(seguimiento_service)
        reporte_controller = ReporteController(reporte_service)

        return MainController(
            login_controller,
            usuario_controller,
            aviso_controller,
            seguimiento_controller,
            reporte_controller
        )

    def _crear_usuario_administrador_inicial(self):
        usuarios = self.main_controller.usuario_controller.obtener_todos_los_usuarios()

        if len(usuarios) == 0:
            self.main_controller.usuario_controller.registrar_usuario(
                "000000000",
                "Administrador",
                "admin@sistema.com",
                "admin123",
                "administrador"
            )

    def mostrar_login(self):
        self._limpiar_ventana()
        self.root.title("Inicio de sesión")

        LoginView(
            self.root,
            self.main_controller.login_controller,
            on_login_success=self.mostrar_sistema_principal
        )

    def mostrar_sistema_principal(self, usuario=None):
        self._limpiar_ventana()
        self.root.title("Sistema de Gestión de Avisos Ciudadanos")

        MainView(
            self.root,
            self.main_controller,
            on_logout=self.mostrar_login
        )

    def _limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def ejecutar(self):
        self.root.mainloop()


def main():
    try:
        app = App()
        app.ejecutar()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar el sistema: {e}")


if __name__ == "__main__":
    main()