# Servicio encargado de generar reportes y estadísticas del sistema.
class ReporteService:
    def __init__(self, aviso_repository):
        self.aviso_repository = aviso_repository

    def obtener_listado_general_avisos(self):
        return self.aviso_repository.get_all()

    def contar_total_avisos(self):
        return len(self.aviso_repository.get_all())

    def contar_avisos_pendientes(self):
        return len(self.aviso_repository.get_by_estado("Pendiente"))

    def contar_avisos_en_proceso(self):
        return len(self.aviso_repository.get_by_estado("En proceso"))

    def contar_avisos_resueltos(self):
        return len(self.aviso_repository.get_by_estado("Resuelto"))

    def obtener_estadisticas_generales(self):
        return {
            "total": self.contar_total_avisos(),
            "pendientes": self.contar_avisos_pendientes(),
            "en_proceso": self.contar_avisos_en_proceso(),
            "resueltos": self.contar_avisos_resueltos()
        }

    def contar_avisos_por_tipo(self):
        conteo = {}

        for aviso in self.aviso_repository.get_all():
            if aviso.tipo_dano not in conteo:
                conteo[aviso.tipo_dano] = 0

            conteo[aviso.tipo_dano] += 1

        return conteo