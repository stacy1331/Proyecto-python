class AvisoController:
    def __init__(self, aviso_service):
        self.aviso_service = aviso_service

    def registrar_aviso(self, codigo, cedula_usuario, tipo_dano, descripcion, ubicacion, fecha):
        self.aviso_service.registrar_aviso(
            codigo,
            cedula_usuario,
            tipo_dano,
            descripcion,
            ubicacion,
            fecha
        )

    def buscar_aviso_por_codigo(self, codigo):
        return self.aviso_service.buscar_aviso_por_codigo(codigo)

    def obtener_todos_los_avisos(self):
        return self.aviso_service.obtener_todos_los_avisos()

    def obtener_avisos_por_usuario(self, cedula_usuario):
        return self.aviso_service.obtener_avisos_por_usuario(cedula_usuario)

    def obtener_avisos_por_estado(self, estado):
        return self.aviso_service.obtener_avisos_por_estado(estado)

    def actualizar_estado_aviso(self, codigo, nuevo_estado):
        self.aviso_service.actualizar_estado_aviso(codigo, nuevo_estado)