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
            seguimiento = Seguimiento.from_dict(item)
            self._seguimientos.append(seguimiento)
            self._seguimientos_by_codigo[seguimiento.codigo_seguimiento] = seguimiento

            if seguimiento.codigo_aviso not in self._seguimientos_by_aviso:
                self._seguimientos_by_aviso[seguimiento.codigo_aviso] = []

            self._seguimientos_by_aviso[seguimiento.codigo_aviso].append(seguimiento)

    def _save(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        data = [seguimiento.to_dict() for seguimiento in self._seguimientos]

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add(self, seguimiento: Seguimiento):
        if seguimiento.codigo_seguimiento in self._seguimientos_by_codigo:
            raise ValueError("Ya existe un seguimiento con ese código.")

        self._seguimientos.append(seguimiento)
        self._seguimientos_by_codigo[seguimiento.codigo_seguimiento] = seguimiento

        if seguimiento.codigo_aviso not in self._seguimientos_by_aviso:
            self._seguimientos_by_aviso[seguimiento.codigo_aviso] = []

        self._seguimientos_by_aviso[seguimiento.codigo_aviso].append(seguimiento)

        self._save()

    def get_by_codigo(self, codigo_seguimiento: str):
        return self._seguimientos_by_codigo.get(codigo_seguimiento)

    def get_by_aviso(self, codigo_aviso: str):
        return list(self._seguimientos_by_aviso.get(codigo_aviso, []))

    def get_all(self):
        return list(self._seguimientos)

    def exists(self, codigo_seguimiento: str) -> bool:
        return codigo_seguimiento in self._seguimientos_by_codigo