class Seguimiento:
    def __init__(self, codigo_seguimiento, codigo_aviso, estado, observacion, fecha_actualizacion, responsable):
        self.codigo_seguimiento = codigo_seguimiento
        self.codigo_aviso = codigo_aviso
        self.estado = estado
        self.observacion = observacion
        self.fecha_actualizacion = fecha_actualizacion
        self.responsable = responsable

    def to_dict(self):
        return {
            "codigo_seguimiento": self.codigo_seguimiento,
            "codigo_aviso": self.codigo_aviso,
            "estado": self.estado,
            "observacion": self.observacion,
            "fecha_actualizacion": self.fecha_actualizacion,
            "responsable": self.responsable
        }

    @staticmethod
    def from_dict(data):
        return Seguimiento(
            data["codigo_seguimiento"],
            data["codigo_aviso"],
            data["estado"],
            data["observacion"],
            data["fecha_actualizacion"],
            data["responsable"]
        )

    def __str__(self):
        return f"{self.codigo_seguimiento} - Aviso: {self.codigo_aviso} - {self.estado}"