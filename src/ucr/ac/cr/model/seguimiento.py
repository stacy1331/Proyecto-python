class Seguimiento:
    def __init__(self, codigo_seguimiento, codigo_aviso, estado, observacion, fecha_actualizacion, responsable):
        self.codigo_seguimiento = codigo_seguimiento
        self.codigo_aviso = codigo_aviso
        self.estado = estado
        self.observacion = observacion
        self.fecha_actualizacion = fecha_actualizacion
        self.responsable = responsable


    def __str__(self):
        return f"Codigo seguimiento: {self.codigo_seguimiento} - Aviso: {self.codigo_aviso} -  Estado - {self.estado} - Observacion: {self.observacion} - Fecha de actualizacion: {self.fecha_actualizacion} - Responsable: {self.responsable}"