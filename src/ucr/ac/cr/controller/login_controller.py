class LoginController:
    def __init__(self, auth_service):
        self.auth_service = auth_service
        self.usuario_actual = None

    def iniciar_sesion(self, correo, contrasena):
        self.usuario_actual = self.auth_service.login(correo, contrasena)
        return self.usuario_actual

    def cerrar_sesion(self):
        self.usuario_actual = None

    def es_administrador(self):
        return self.auth_service.es_administrador(self.usuario_actual)

    def es_ciudadano(self):
        return self.auth_service.es_ciudadano(self.usuario_actual)