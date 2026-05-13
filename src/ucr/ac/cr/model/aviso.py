class Aviso:
    def __init__(self, codigo, cedula_usuario, tipo_dano, descripcion, ubicacion, fecha, estado="Pendiente"):
        self.codigo = codigo
        self.cedula_usuario = cedula_usuario
        self.tipo_dano = tipo_dano
        self.descripcion = descripcion
        self.ubicacion = ubicacion
        self.fecha = fecha
        self.estado = estado

    def __str__(self):
        return f"Codigo: {self.codigo} - Cedula: {self.cedula_usuario} - Tipo daño: {self.tipo_dano} - Descripcion: {self.descripcion} - Ubicacion: {self.ubicacion} - Fecha: {self.fecha} - Estado: {self.estado}"