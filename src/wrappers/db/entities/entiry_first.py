import logging

from src.wrappers.db.base_controller import BaseController


class TableA(BaseController):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self._table_name = "TableA"
        self._table = self._db.metadata.tables[self._table_name]
        self._table_definition = {
            "id": ["int"],
            "name": ["str"],
            "description": ["str", "NoneType"],
            "created_at": ["datetime"],
        }


