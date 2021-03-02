"""
flatlanddb.py - Loads the existing flatland database
"""
import sys
import logging
import logging.config
from pathlib import Path
from sqlalchemy import create_engine, MetaData
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def Create_relvars():
    """
    A relvar is a relational variable as defined by C.J. Date and Hugh Darwin.
    In the world of SQL it is effectively a table. Here we define all the relvars
    and then have the corresponding table schemas populated into the Sqlalchemy
    metadata.
    """
    from flatland.database import relvars
    FlatlandDB.Relvars = relvars.define(FlatlandDB)
    FlatlandDB.MetaData.create_all(FlatlandDB.Engine)


def Populate():
    """
    Assign a value to each Flatland relvar (table). A value consists of a set of relations.
    In Sqlalchemy terms, the tables are all updated with initial row data.
    """
    # We need to append each population subirectory to our module search path
    # because when we iterate through the file names in our relvar dictionary
    # we don't know which file is in which subdirectory. So we can't just
    # refer to each population module by the same path
    here = Path(__file__).parent / "population"  # Adjacent population directory
    pop_dirs = [  # Subdirectories organizing all population modules
        here / "connector", here / "decorator", here / "drawing", here / "node", here / "sheet"
    ]
    # Convert each Path object to a string and tack it on the end of our module search path
    sys.path.extend([str(p) for p in pop_dirs])

    # Iterate through the relvar dictionary to get each population and the table it goes into
    for instances, relvar in FlatlandDB.Relvars.items():
        # Set i to the initial population of row values (set of relation values)
        i = __import__(instances + '_instances')  # Each population filename ends with '_instances.py'
        if i.population:  # A computed relations may start with an empty population, so skip the insert if empty
            FlatlandDB.Connection.execute(relvar.insert(), i.population)  # Sqlalchemy populates the table schema


class FlatlandDB:
    """
    Flatland database containing all predefined Flatland data. We want to avoid having any predefined
    data declared in the code itself.

    Here we use Sqlalchemy to create the database engine and connection

        Attributes

        - File -- Local directory location of the sqlite3 database file
        - Metadata -- Sqlalchemy metadata
        - Connection -- Sqlalchemy database connection
        - Engine -- Sqlalchemy database engine
        - Relvars -- Dictionary of all relvar names and values (table names and row populations)
    """
    File = Path(__file__).parent / "flatland.db"
    LogFile = Path(__file__).parent / "db.log"
    MetaData = None
    Connection = None
    Engine = None
    Relvars = None

    def __init__(self, rebuild: bool):
        """
        Create the sqlite3 database using Sqlalchemy

        :param rebuild: During development this will usually be true.  For deployment it should be false.
        """
        self.logger = logging.getLogger(__name__)
        self.rebuild = rebuild

        if self.rebuild:  # DB rebuild requested
            # Start with a fresh database
            if FlatlandDB.File.exists():
                FlatlandDB.File.unlink()
        else:  # No rebuild requested
            if FlatlandDB.File.exists():
                self.logger.info("Using existing database")
            else:  # We're going to have to rebuild it anyway
                self.rebuild = True
                self.logger.info("No db file, rebuilding flatland database")

        db_path_str = str( FlatlandDB.File )

        # Configure sql logger
        db_file_handler = logging.FileHandler(FlatlandDB.LogFile, 'w')
        # db_file_handler.setLevel(logging.DEBUG)
        dblogger = logging.getLogger('sqlalchemy.engine')
        dblogger.setLevel(logging.DEBUG)
        dblogger.addHandler(db_file_handler)
        dblogger.propagate = False  # To keep sql events from bleeding into the flatland log

        FlatlandDB.Engine = create_engine(f'sqlite:///{db_path_str}', echo=False)
        FlatlandDB.Connection = FlatlandDB.Engine.connect()
        FlatlandDB.MetaData = MetaData(FlatlandDB.Engine)
        if self.rebuild:
            self.logger.info(f"Re-creating database file at: {db_path_str}")
            Create_relvars()
            Populate()
        else:
            # Just interrogate the existing database to get all the relvar/table names
            FlatlandDB.MetaData.reflect()


if __name__ == "__main__":
    #  Rebuild the database
    FlatlandDB()
