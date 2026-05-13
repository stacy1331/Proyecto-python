class Aviso:
    def __init__(self, codigo, cedula_usuario, tipo_dano, descripcion, ubicacion, fecha, estado="Pendiente"):
        self.codigo = codigo
        self.cedula_usuario = cedula_usuario
        self.tipo_dano = tipo_dano
        self.descripcion = descripcion
        self.ubicacion = ubicacion
        self.fecha = fecha
        self.estado = estado

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "cedula_usuario": self.cedula_usuario,
            "tipo_dano": self.tipo_dano,
            "descripcion": self.descripcion,
            "ubicacion": self.ubicacion,
            "fecha": self.fecha,
            "estado": self.estado
        }

    @staticmethod
    def from_dict(data):
        return Aviso(
            data["codigo"],
            data["cedula_usuario"],
            data["tipo_dano"],
            data["descripcion"],
            data["ubicacion"],
            data["fecha"],
            data.get("estado", "Pendiente")
        )

    def __str__(self):
        return f"{self.codigo} - {self.tipo_dano} - {self.estado}"