class UsuarioController:
    def __init__(self, usuario_service):
        self.usuario_service = usuario_service

    def registrar_usuario(self, cedula, nombre, correo, contrasena, rol):
        self.usuario_service.registrar_usuario(
            cedula,
            nombre,
            correo,
            contrasena,
            rol
        )

    def buscar_usuario_por_cedula(self, cedula):
        return self.usuario_service.buscar_usuario_por_cedula(cedula)

    def buscar_usuario_por_correo(self, correo):
        return self.usuario_service.buscar_usuario_por_correo(correo)

    def obtener_todos_los_usuarios(self):
        return self.usuario_service.obtener_todos_los_usuarios()