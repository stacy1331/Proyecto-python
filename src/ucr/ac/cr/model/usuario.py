class Usuario:
    def __init__(self, cedula, nombre, correo, contrasena, rol):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol

    def __str__(self):
        return f"Cedula: {self.cedula} - Nombre: {self.nombre} - Correo: {self.correo} - Contraseña: {self.contrasena} - Rol: {self.rol}"