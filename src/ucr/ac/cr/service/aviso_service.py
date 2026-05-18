from src.ucr.ac.cr.model.aviso import Aviso

# Servicio encargado de la lógica de negocio relacionada con los avisos.
class AvisoService:
    def __init__(self, aviso_repository, usuario_repository):
        self.aviso_repository = aviso_repository
        self.usuario_repository = usuario_repository

    def registrar_aviso(self, codigo: str, cedula_usuario: str, tipo_dano: str,
                        descripcion: str, ubicacion: str, fecha: str):
        if not codigo.strip():
            raise ValueError("El código del aviso no puede estar vacío.")

        if not cedula_usuario.strip():
            raise ValueError("La cédula del usuario no puede estar vacía.")

        if not tipo_dano.strip():
            raise ValueError("El tipo de daño no puede estar vacío.")

        if not descripcion.strip():
            raise ValueError("La descripción no puede estar vacía.")

        if not ubicacion.strip():
            raise ValueError("La ubicación no puede estar vacía.")

        if not fecha.strip():
            raise ValueError("La fecha no puede estar vacía.")

        if not self.usuario_repository.exists(cedula_usuario):
            raise ValueError("No existe un usuario registrado con esa cédula.")

        aviso = Aviso(
            codigo,
            cedula_usuario,
            tipo_dano,
            descripcion,
            ubicacion,
            fecha,
            "Pendiente"
        )

        self.aviso_repository.add(aviso)

    def buscar_aviso_por_codigo(self, codigo: str):
        if not codigo.strip():
            raise ValueError("El código del aviso no puede estar vacío.")

        aviso = self.aviso_repository.get_by_codigo(codigo)

        if aviso is None:
            raise ValueError("No existe un aviso con ese código.")

        return aviso

    def obtener_todos_los_avisos(self):
        return self.aviso_repository.get_all()

    def obtener_avisos_por_usuario(self, cedula_usuario: str):
        if not cedula_usuario.strip():
            raise ValueError("La cédula del usuario no puede estar vacía.")

        if not self.usuario_repository.exists(cedula_usuario):
            raise ValueError("No existe un usuario registrado con esa cédula.")

        return self.aviso_repository.get_by_usuario(cedula_usuario)

    def obtener_avisos_por_estado(self, estado: str):
        if not estado.strip():
            raise ValueError("El estado no puede estar vacío.")

        return self.aviso_repository.get_by_estado(estado)

    def actualizar_estado_aviso(self, codigo: str, nuevo_estado: str):
        estados_validos = ["Pendiente", "En proceso", "Resuelto"]

        if nuevo_estado not in estados_validos:
            raise ValueError("El estado debe ser Pendiente, En proceso o Resuelto.")

        aviso = self.aviso_repository.get_by_codigo(codigo)

        if aviso is None:
            raise ValueError("No existe un aviso con ese código.")

        aviso.estado = nuevo_estado
        self.aviso_repository.update(aviso)