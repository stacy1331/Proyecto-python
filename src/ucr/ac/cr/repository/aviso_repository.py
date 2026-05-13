import json
import os
from src.ucr.ac.cr.model.aviso import Aviso


class AvisoRepository:
    def __init__(self, filename="data/avisos.json"):
        self.filename = filename
        self._avisos = []
        self._avisos_by_codigo = {}
        self._avisos_by_usuario = {}
        self._avisos_by_estado = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            return

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            aviso = Aviso.from_dict(item)
            self._agregar_a_memoria(aviso)

    def _save(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        data = [aviso.to_dict() for aviso in self._avisos]

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def _agregar_a_memoria(self, aviso: Aviso):
        self._avisos.append(aviso)
        self._avisos_by_codigo[aviso.codigo] = aviso

        if aviso.cedula_usuario not in self._avisos_by_usuario:
            self._avisos_by_usuario[aviso.cedula_usuario] = []
        self._avisos_by_usuario[aviso.cedula_usuario].append(aviso)

        if aviso.estado not in self._avisos_by_estado:
            self._avisos_by_estado[aviso.estado] = []
        self._avisos_by_estado[aviso.estado].append(aviso)

    def add(self, aviso: Aviso):
        if aviso.codigo in self._avisos_by_codigo:
            raise ValueError("Ya existe un aviso con ese código.")

        self._agregar_a_memoria(aviso)
        self._save()

    def get_by_codigo(self, codigo: str):
        return self._avisos_by_codigo.get(codigo)

    def get_by_usuario(self, cedula_usuario: str):
        return list(self._avisos_by_usuario.get(cedula_usuario, []))

    def get_by_estado(self, estado: str):
        return list(self._avisos_by_estado.get(estado, []))

    def get_all(self):
        return list(self._avisos)

    def exists(self, codigo: str) -> bool:
        return codigo in self._avisos_by_codigo

    def update(self, aviso_actualizado: Aviso):
        if aviso_actualizado.codigo not in self._avisos_by_codigo:
            raise ValueError("No existe un aviso con ese código.")

        for index, aviso in enumerate(self._avisos):
            if aviso.codigo == aviso_actualizado.codigo:
                self._avisos[index] = aviso_actualizado
                break

        self._rebuild_indexes()
        self._save()

    def _rebuild_indexes(self):
        self._avisos_by_codigo = {}
        self._avisos_by_usuario = {}
        self._avisos_by_estado = {}

        avisos_actuales = list(self._avisos)
        self._avisos = []

        for aviso in avisos_actuales:
            self._agregar_a_memoria(aviso)