from src.ucr.ac.cr.model.usuario import Usuario


class UsuarioService:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def registrar_usuario(self, cedula: str, nombre: str, correo: str, contrasena: str, rol: str):
        if not cedula.strip():
            raise ValueError("La cédula no puede estar vacía.")

        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if not correo.strip():
            raise ValueError("El correo no puede estar vacío.")

        if not contrasena.strip():
            raise ValueError("La contraseña no puede estar vacía.")

        if not rol.strip():
            raise ValueError("El rol no puede estar vacío.")

        roles_validos = ["administrador", "ciudadano"]

        if rol.lower() not in roles_validos:
            raise ValueError("El rol debe ser administrador o ciudadano.")

        usuario = Usuario(
            cedula,
            nombre,
            correo,
            contrasena,
            rol.lower()
        )

        self.usuario_repository.add(usuario)

    def buscar_usuario_por_cedula(self, cedula: str):
        if not cedula.strip():
            raise ValueError("La cédula no puede estar vacía.")

        usuario = self.usuario_repository.get_by_cedula(cedula)

        if usuario is None:
            raise ValueError("No existe un usuario con esa cédula.")

        return usuario

    def buscar_usuario_por_correo(self, correo: str):
        if not correo.strip():
            raise ValueError("El correo no puede estar vacío.")

        usuario = self.usuario_repository.get_by_correo(correo)

        if usuario is None:
            raise ValueError("No existe un usuario con ese correo.")

        return usuario

    def obtener_todos_los_usuarios(self):
        return self.usuario_repository.get_all()