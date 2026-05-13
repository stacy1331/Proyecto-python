class Usuario:
    def __init__(self, cedula, nombre, correo, contrasena, rol):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol

    def to_dict(self):
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "correo": self.correo,
            "contrasena": self.contrasena,
            "rol": self.rol
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            data["cedula"],
            data["nombre"],
            data["correo"],
            data["contrasena"],
            data["rol"]
        )

    def __str__(self):
        return f"{self.nombre} - {self.rol}"