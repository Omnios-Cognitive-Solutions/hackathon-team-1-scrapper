import logging
import pandas

from sqlalchemy import insert, update

from src.wrappers.db.connect import db_connection
from src.wrappers.db.exception import DBException


class BaseController:
    LOAD_INTO_DATAFRAME_DEFAULT = False

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._db = db_connection

        # string with table name from the database
        self._table_name = ""

        # __table should have the table metadata: self._db.metadata.tables[self._table_name]
        self._table = None

        # __table_description should be a dict with the table columns description:
        # {'column_name': [<allowed types>, ...]} -> {"user_name": ["str", "NoneType"]}
        # Leave it as None to skip verification
        self._table_definition = None

    @DBException.error_handling
    def _is_valid(self, data):
        """
        Validates the input data for the current table.
        :param data: Dict with the data to be validated. {column_name: value}
        :return: True if input data is valid, False otherwise.
        """
        if not self._table_definition:
            self._logger.warning("Table definition not set, skipping input validation.")
            return True

        for column_name, column_value in data.items():
            if column_name not in self._table_definition:
                self._logger.warning(
                    f"Column name '{column_name}' not defined for table {self._table_name}"
                )
                continue

            provided_type = type(column_value).__name__
            allowed_types = self._table_definition[column_name]
            if provided_type not in allowed_types:
                could_be_converted = False
                for allowed_type in allowed_types:
                    try:
                        if allowed_type == "NoneType":
                            continue
                        data[column_name] = eval(allowed_type)(column_value)
                        could_be_converted = True
                    except (ValueError, TypeError):
                        continue
                if could_be_converted:
                    self._logger.info(
                        f"Column '{column_name}': value '{column_value}' "
                        f"type '{provided_type}' "
                        f"was converted to {type(data[column_name]).__name__}"
                    )
                    continue

                self._logger.error(
                    f"Column '{column_name}': value '{column_value}' "
                    f"is not of type {self._table_definition[column_name]}"
                )
                return False

        return True

    @DBException.error_handling
    def insert(self, data):
        """
        Inserts a new competitor into the database.
        :param data: Dict with the object data to insert into the database
        :return: DB response
        """
        self._logger.info(f"Inserting '{data}' into {self._table_name}")

        if not self._is_valid(data):
            raise DBException(f"Invalid data '{data}' for table {self._table_name}")

        if self._table is None:
            self._logger.error(f"Table {self._table_name} not initialized")
            return None

        data_to_insert = data.copy()
        data_to_insert = {
            key: value for key, value in data_to_insert.items()
            if key in self._table_definition
        }
        with self._db.Session(self._db) as session:
            self._logger.debug(f"Inserting '{data_to_insert}' into {self._table_name}")
            statement = insert(self._table).values(**data_to_insert)
            response = session.execute(statement)

        return response

    @DBException.error_handling
    def get(self, identifier_tuple, load_into_dataframe=LOAD_INTO_DATAFRAME_DEFAULT):
        """
        Returns the object with the specified id.
        :param identifier_tuple: Identifier of the competitor to return
                                (column_name, column_value)
        :param load_into_dataframe: If True, returns a pandas DataFrame with the data
        :return: Competitor object
        """
        self._logger.info(f"Getting '{identifier_tuple}' from {self._table_name}")

        if not self._is_valid({identifier_tuple[0]: identifier_tuple[1]}):
            raise DBException(f"Invalid data '{identifier_tuple}' for table {self._table_name}")

        if self._table is None:
            self._logger.error(f"Table {self._table_name} not initialized")
            return None

        with self._db.Session(self._db) as session:
            query = session.query(self._table)\
                .filter(getattr(self._table.columns, identifier_tuple[0]) == identifier_tuple[1])

            if load_into_dataframe:
                response = pandas.read_sql(query.statement, session.bind)
            else:
                response = query.all()

        if len(response) == 0:
            return None
        elif len(response) > 1:
            self._logger.error(f"Multiple objects found for {identifier_tuple}. Using first one.")
        return response[0]

    @DBException.error_handling
    def select(self, filters, load_into_dataframe=LOAD_INTO_DATAFRAME_DEFAULT):
        """
        Returns the competitor with the specified identifier.
        :param filters: Dict containing the column_name: column_value pairs to filter
        :param load_into_dataframe: If True, returns a pandas DataFrame with the data
        :return: Competitor object
        """
        self._logger.info(f"Selecting '{filters}' from the {self._table_name} table")

        if not self._is_valid(filters):
            raise DBException(f"Invalid data '{filters}' for table {self._table_name}")

        if self._table is None:
            self._logger.error(f"Table {self._table_name} not initialized")
            return None

        with self._db.Session(self._db) as session:
            query = session.query(self._table).filter_by(**filters)

            if load_into_dataframe:
                response = pandas.read_sql(query.statement, session.bind)
            else:
                response = query.all()
        return response

    @DBException.error_handling
    def list(self, load_into_dataframe=LOAD_INTO_DATAFRAME_DEFAULT):
        """
        Returns a list of all objects in the table.
        :param load_into_dataframe: If True, returns a pandas DataFrame with the data.
        :return: List of Competitor objects
        """
        return self.select({}, load_into_dataframe)

    @DBException.error_handling
    def update(self, identifier_tuple, data):
        """
        Updates the object with the specified identifier_tuple.
        :param identifier_tuple: Identifier tuple of the object to update
        :param data: Dict containing the column_name: column_value pairs
                           to update into the table
        return: DB response
        """
        self._logger.info(f"Updating '{identifier_tuple}' with {data} in the {self._table_name}")

        if not self._is_valid({identifier_tuple[0]: identifier_tuple[1]}):
            raise DBException(f"Invalid data '{identifier_tuple}' for table {self._table_name}")
        if not self._is_valid(data):
            raise DBException(f"Invalid data '{data}' for table {self._table_name}")

        if self._table is None:
            self._logger.error(f"Table {self._table_name} not initialized")
            return None

        data_to_update = data.copy()
        data_to_update = {
            key: value for key, value in data_to_update.items()
            if key in self._table_definition
        }
        with self._db.Session(self._db) as session:
            statement = update(self._table)\
                .where(getattr(self._table.columns, identifier_tuple[0]) == identifier_tuple[1])\
                .values(**data_to_update)
            response = session.execute(statement)
        return response
