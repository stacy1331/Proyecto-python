class SeguimientoController:
    def __init__(self, seguimiento_service):
        self.seguimiento_service = seguimiento_service

    def registrar_seguimiento(self, codigo_seguimiento, codigo_aviso, estado, observacion, fecha_actualizacion, responsable):
        self.seguimiento_service.registrar_seguimiento(
            codigo_seguimiento,
            codigo_aviso,
            estado,
            observacion,
            fecha_actualizacion,
            responsable
        )

    def buscar_seguimiento_por_codigo(self, codigo_seguimiento):
        return self.seguimiento_service.buscar_seguimiento_por_codigo(codigo_seguimiento)

    def obtener_seguimientos_por_aviso(self, codigo_aviso):
        return self.seguimiento_service.obtener_seguimientos_por_aviso(codigo_aviso)

    def obtener_todos_los_seguimientos(self):
        return self.seguimiento_service.obtener_todos_los_seguimientos()