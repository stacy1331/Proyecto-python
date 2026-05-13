class ReporteController:
    def __init__(self, reporte_service):
        self.reporte_service = reporte_service

    def obtener_listado_general_avisos(self):
        return self.reporte_service.obtener_listado_general_avisos()

    def obtener_estadisticas_generales(self):
        return self.reporte_service.obtener_estadisticas_generales()

    def contar_avisos_por_tipo(self):
        return self.reporte_service.contar_avisos_por_tipo()