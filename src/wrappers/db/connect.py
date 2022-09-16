import logging

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from src.config import config
from src.wrappers.db.exception import DBException

logger = logging.getLogger(__name__)


class DBConnection:

    @DBException.error_handling
    def __init__(self) -> None:
        """
        Initializes a SQL engine connected to the DB
        and a SQLAlchemy Session Maker using this engine.
        """
        self.config = config

        # pylint: disable=consider-using-f-string
        self.url = "{schema}://{username}:{password}@{host}:{port}/{db}".format(
                schema=self.config.get('MYSQL', 'schema'),
                username=self.config.get('MYSQL', 'username'),
                password=self.config.get('MYSQL', 'password'),
                host=self.config.get('MYSQL', 'host'),
                port=self.config.get('MYSQL', 'port'),
                db=self.config.get('MYSQL', 'db')
            )

        self.__engine = self.__create_db_engine()
        self.session_maker = self.__initialize_session_maker()
        self.metadata = self.__retrieve_db_metadata()

    @DBException.error_handling
    def __create_db_engine(self):
        """
        Creates a DB engine connected to the url set in the attributes.

        :return: The DB engine
        """
        url = self.url

        try:
            engine = create_engine(url, echo=False)
            return engine
        except Exception as e:
            logger.error(f"Unexpected error creating DB engine: '{e}'")
            raise e

    @DBException.error_handling
    def __initialize_session_maker(self):
        """
        Initializes a SQLAlchemy Session Maker using the engine stored in the attributes.

        :return: The Session Maker
        """
        engine = self.__engine

        session_maker = sessionmaker()
        session_maker.configure(bind=engine)
        return session_maker

    @DBException.error_handling
    def __retrieve_db_metadata(self):
        """
        Retrieves all the DB MetaData from the engine set in the attributes.

        :return: The DB metadata
        """
        engine = self.__engine

        metadata = MetaData(bind=engine)
        metadata.reflect()
        return metadata

    class Session:
        def __init__(self, db):
            self.__db = db
            self.session = None

        @DBException.error_handling
        def __enter__(self):
            """
            Starts a DB session using the Session Maker in the attributes.
            If a session has already been started, return it instead so only
            one session can be used per instance.

            :return: The session that has been created
            """

            session_maker = self.__db.session_maker

            if self.session is None:
                session = session_maker()
                self.session = session
            else:
                session = self.session
            return session

        @DBException.error_handling
        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            Closes the session if it has been started.
            """

            session = self.session

            if session is not None:
                if exc_type is not None:
                    session.rollback()
                else:
                    session.commit()
                session.close()
                self.session = None

    @DBException.error_handling
    def execute_raw_query(self, sql_query, parameters=None):
        """
        Executes a raw sql query using the engine
        """
        with self.__engine.connect() as connection:
            if parameters is None:
                result = connection.execute(sql_query)
            else:
                result = connection.execute(sql_query, parameters)
        return result


db_connection = DBConnection()
