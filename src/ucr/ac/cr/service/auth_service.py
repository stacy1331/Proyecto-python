class AuthService:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def login(self, correo: str, contrasena: str):
        if not correo.strip():
            raise ValueError("El correo no puede estar vacío.")

        if not contrasena.strip():
            raise ValueError("La contraseña no puede estar vacía.")

        usuario = self.usuario_repository.get_by_correo(correo)

        if usuario is None:
            raise ValueError("El usuario no existe.")

        if usuario.contrasena != contrasena:
            raise ValueError("La contraseña es incorrecta.")

        return usuario

    def es_administrador(self, usuario):
        return usuario is not None and usuario.rol.lower() == "administrador"

    def es_ciudadano(self, usuario):
        return usuario is not None and usuario.rol.lower() == "ciudadano"