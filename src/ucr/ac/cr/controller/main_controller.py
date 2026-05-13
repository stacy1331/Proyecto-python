class MainController:
    def __init__(self, login_controller, usuario_controller, aviso_controller, seguimiento_controller, reporte_controller):
        self.login_controller = login_controller
        self.usuario_controller = usuario_controller
        self.aviso_controller = aviso_controller
        self.seguimiento_controller = seguimiento_controller
        self.reporte_controller = reporte_controller