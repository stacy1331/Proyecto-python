import json
import os
from src.ucr.ac.cr.model.usuario import Usuario

# Repositorio encargado de administrar los usuarios del sistema.
class UsuarioRepository:
    def __init__(self, filename="data/usuarios.json"):
        self.filename = filename

        # Estructuras en memoria para almacenar y buscar usuarios rápidamente.
        self._usuarios = []
        self._usuarios_by_cedula = {}

        self._usuarios_by_correo = {}
        # Carga automática de usuarios desde el archivo JSON.
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            return

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            usuario = Usuario(
                item["cedula"],
                item["nombre"],
                item["correo"],
                item["contrasena"],
                item["rol"]
            )

            self._usuarios.append(usuario)
            self._usuarios_by_cedula[usuario.cedula] = usuario
            self._usuarios_by_correo[usuario.correo] = usuario

    def _save(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        data = []
        # Convierte los objetos Usuario en formato JSON.
        for usuario in self._usuarios:
            data.append({
                "cedula": usuario.cedula,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "contrasena": usuario.contrasena,
                "rol": usuario.rol
            })

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add(self, usuario: Usuario):
        if usuario.cedula in self._usuarios_by_cedula:
            raise ValueError("Ya existe un usuario con esa cédula.")

        if usuario.correo in self._usuarios_by_correo:
            raise ValueError("Ya existe un usuario con ese correo.")

        self._usuarios.append(usuario)
        self._usuarios_by_cedula[usuario.cedula] = usuario
        self._usuarios_by_correo[usuario.correo] = usuario

        self._save()

    def get_by_cedula(self, cedula: str):
        return self._usuarios_by_cedula.get(cedula)

    def get_by_correo(self, correo: str):
        return self._usuarios_by_correo.get(correo)

    def get_all(self):
        return list(self._usuarios)

    def exists(self, cedula: str) -> bool:
        return cedula in self._usuarios_by_cedula