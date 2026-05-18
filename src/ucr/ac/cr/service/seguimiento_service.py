from src.ucr.ac.cr.model.seguimiento import Seguimiento

# Servicio encargado de la lógica de negocio relacionada con los seguimientos.
class SeguimientoService:
    def __init__(self, seguimiento_repository, aviso_repository):
        self.seguimiento_repository = seguimiento_repository
        self.aviso_repository = aviso_repository

    def registrar_seguimiento(self, codigo_seguimiento: str, codigo_aviso: str,
                              estado: str, observacion: str,
                              fecha_actualizacion: str, responsable: str):
        if not codigo_seguimiento.strip():
            raise ValueError("El código del seguimiento no puede estar vacío.")

        if not codigo_aviso.strip():
            raise ValueError("El código del aviso no puede estar vacío.")

        if not estado.strip():
            raise ValueError("El estado no puede estar vacío.")

        if not observacion.strip():
            raise ValueError("La observación no puede estar vacía.")

        if not fecha_actualizacion.strip():
            raise ValueError("La fecha de actualización no puede estar vacía.")

        if not responsable.strip():
            raise ValueError("El responsable no puede estar vacío.")

        estados_validos = ["Pendiente", "En proceso", "Resuelto"]

        if estado not in estados_validos:
            raise ValueError("El estado debe ser Pendiente, En proceso o Resuelto.")

        aviso = self.aviso_repository.get_by_codigo(codigo_aviso)

        if aviso is None:
            raise ValueError("No existe un aviso con ese código.")

        seguimiento = Seguimiento(
            codigo_seguimiento,
            codigo_aviso,
            estado,
            observacion,
            fecha_actualizacion,
            responsable
        )

        self.seguimiento_repository.add(seguimiento)

        aviso.estado = estado
        self.aviso_repository.update(aviso)

    def buscar_seguimiento_por_codigo(self, codigo_seguimiento: str):
        if not codigo_seguimiento.strip():
            raise ValueError("El código del seguimiento no puede estar vacío.")

        seguimiento = self.seguimiento_repository.get_by_codigo(codigo_seguimiento)

        if seguimiento is None:
            raise ValueError("No existe un seguimiento con ese código.")

        return seguimiento

    def obtener_seguimientos_por_aviso(self, codigo_aviso: str):
        if not codigo_aviso.strip():
            raise ValueError("El código del aviso no puede estar vacío.")

        if not self.aviso_repository.exists(codigo_aviso):
            raise ValueError("No existe un aviso con ese código.")

        return self.seguimiento_repository.get_by_aviso(codigo_aviso)

    def obtener_todos_los_seguimientos(self):
        return self.seguimiento_repository.get_all()