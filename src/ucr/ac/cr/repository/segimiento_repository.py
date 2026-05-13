import json
import os
from src.ucr.ac.cr.model.seguimiento import Seguimiento


class SeguimientoRepository:
    def __init__(self, filename="data/seguimientos.json"):
        self.filename = filename
        self._seguimientos = []
        self._seguimientos_by_codigo = {}
        self._seguimientos_by_aviso = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            return

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            seguimiento = Seguimiento(
                item["codigo_seguimiento"],
                item["codigo_aviso"],
                item["estado"],
                item["observacion"],
                item["fecha_actualizacion"],
                item["responsable"]
            )

            self._agregar_a_memoria(seguimiento)

    def _save(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        data = []

        for seguimiento in self._seguimientos:
            data.append({
                "codigo_seguimiento": seguimiento.codigo_seguimiento,
                "codigo_aviso": seguimiento.codigo_aviso,
                "estado": seguimiento.estado,
                "observacion": seguimiento.observacion,
                "fecha_actualizacion": seguimiento.fecha_actualizacion,
                "responsable": seguimiento.responsable
            })

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def _agregar_a_memoria(self, seguimiento):
        self._seguimientos.append(seguimiento)
        self._seguimientos_by_codigo[seguimiento.codigo_seguimiento] = seguimiento

        if seguimiento.codigo_seguimiento not in self._seguimientos_by_aviso:
            self._seguimientos_by_aviso[seguimiento.codigo_seguimiento] = []
        self._seguimientos_by_aviso[seguimiento.codigo_aviso].append(seguimiento)

    def add(self, seguimiento: Seguimiento):
        if seguimiento.codigo_seguimiento in self._seguimientos_by_codigo:
            raise ValueError("Ya existe un seguimiento con ese código.")

        self._agregar_a_memoria(seguimiento)
        self._save()

    def get_by_codigo(self, codigo_seguimiento: str):
        return self._seguimientos_by_codigo.get(codigo_seguimiento)

    def get_by_aviso(self, codigo_aviso: str):
        return list(self._seguimientos_by_aviso.get(codigo_aviso, []))

    def get_all(self):
        return list(self._seguimientos)

    def exists(self, codigo_seguimiento: str) -> bool:
        return codigo_seguimiento in self._seguimientos_by_codigo