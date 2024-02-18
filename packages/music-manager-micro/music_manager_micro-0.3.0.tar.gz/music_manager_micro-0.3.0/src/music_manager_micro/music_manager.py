"""Module providing the MusicManager class"""
import os
import logging
import sqlite3
from pathlib import Path
from ._file import File as F


class MusicManager():
    """Class to manage finding media files within a directory"""
    app_name = 'MusicManagerMicro'

    # Directory and files
    root_config_dir: str = os.path.join(
        str(Path.home()), ".config/", app_name)
    root_cache_dir: str = os.path.join(
        str(Path.home()), ".cache/", app_name)
    library_cache_file = 'library.db'
    active_library_config_dir: str
    active_library_cache_dir: str

    library = ''
    media_path: str

    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)
    DEBUG = False

    def __debug(self, message):
        if self.DEBUG:
            logging.debug(str(message))

    def __init__(self, library: str = 'library', media_dir: str = '.'):
        self.set_library(library)
        self.set_root_dir(media_dir)

    def set_library(self, library: str) -> None:
        """
        Used to set which library dataset we are using.
        Will create a sqlite db to store results in cache directory
        """
        self.library = library
        self._update_root_dir()

    def set_root_dir(self, media_dir: str):
        """
        Used to set the path to search for supported media files
        Can be relative or absolute, as long as the provided string resolves to a directory
        """
        self.media_path = media_dir

    def _update_root_dir(self) -> None:
        self.active_library_config_dir = self._generate_library_dir()
        os.makedirs(self.active_library_config_dir, exist_ok=True)

    def _generate_library_dir(self) -> str:
        return os.path.join(
            self.root_cache_dir, self.library)

    ###
    # DB functions
    ###
    def instantiate_sqlite_table(self, file_name: str) -> sqlite3.Cursor:
        """Sets up the required sqlite db"""
        con = sqlite3.connect(file_name)
        cur = con.cursor()
        res = cur.execute("SELECT ? FROM sqlite_master", ('music',))
        is_created = res.fetchone()
        if is_created is None:
            cur.execute("CREATE TABLE music(mtime, file_path type UNIQUE)")
        return cur

    def db_get_all(self, cur: sqlite3.Cursor) -> list:
        """Returns all values from the current db"""
        res = cur.execute("SELECT * FROM music")
        ret_val = res.fetchall()
        # print(f'db_get_all ret val {ret_val}')
        return [] if ret_val is None else ret_val

    def db_insert(self, cur: sqlite3.Cursor, entry: tuple):
        """Places an entry into the db with two values
        mtime and file_path from the tuple
        will match on file_path to update existing rows"""
        sub_obj = {
            'mtime': entry[0],
            'file_path': entry[1]
        }
        cur.execute("""
                    INSERT INTO music(mtime,file_path) 
                    VALUES (:mtime, :file_path) 
                    ON CONFLICT(file_path) 
                    DO UPDATE SET mtime=:mtime, file_path=:file_path
                    """,
                    sub_obj)

    def db_delete(self, cur: sqlite3.Cursor) -> None:
        """Performs a delete on all rows in the music db"""
        cur.execute("DELETE FROM music")

    def db_commit(self, sql_con: sqlite3.Connection) -> None:
        """Commits all outstanding statements"""
        sql_con.commit()

    def db_close(self, sql_con: sqlite3.Connection) -> None:
        """Closes the connection"""
        sql_con.close()

    ###
    # Utils
    ###
    extensions = ('.mp3', '.flac')

    def get_files_from_folder(self, folder: str) -> list:
        """Returns the list of all files recursively in a directory"""
        ret_val = []
        for r, _, f in os.walk(folder):
            for file in f:
                if file.endswith(self.extensions):
                    ret_val.append(f'{r}/{file}')
        return ret_val

    ###
    # Program Functions
    ###

    library_list = []

    def build_entry(self, file_path: str) -> tuple | None:
        """docstring"""
        try:
            file = F(file_path, '', '', os.path.getmtime(file_path))
            return (file.mtime, file.path)
        except FileNotFoundError as err:
            self.__debug(f"Error in build_entry {err=}, {type(err)=}")
            return None

    def build_list(self, root_path: str) -> list:
        """Given a path string constructs a list of File objects"""
        self.library_list = []
        # return library_list
        files = self.get_files_from_folder(root_path)
        self.__debug(f"Found {len(files)} files")
        for f in files:
            self.__debug(f)
            self.library_list.append(self.build_entry(f))
        # __save_list()
        return self.library_list

    def execute(self) -> list[tuple[float, str]]:
        """
        Use to fully walk the directory and find all compatible
        media files. Will store the results in the standard
        cache directory.

        :returns: List of tuples representing the float mtime
            of the media file and path
        """
        return_value = self.build_list(self.media_path)
        self._save_list()
        return return_value

    def reset_library(self) -> None:
        """
        Clears the cached results
        """
        _file = self.__build_file_path()
        cur = self.instantiate_sqlite_table(_file)
        self.db_delete(cur)
        self.db_commit(cur.connection)
        self.db_close(cur.connection)

    def get_list(self) -> list[tuple[float, str]]:
        """
        Returns the list for the given library without running 
        the search

        :returns: List of tuples representing the float mtime
            of the media file and path
        """
        self._load_list()
        return self.library_list

    def __build_file_path(self) -> str:
        return os.path.join(self.active_library_config_dir, self.library_cache_file)

    def _load_list(self) -> None:
        _file = self.__build_file_path()
        cur = self.instantiate_sqlite_table(_file)
        self.library_list = self.db_get_all(cur)

    def _save_list(self) -> None:
        """Uses a filepath + filename string and content string overwrites the resulting file"""
        content = self.library_list
        write_file = self.__build_file_path()
        if os.path.dirname(write_file) != '':
            os.makedirs(os.path.dirname(write_file), exist_ok=True)
        cur = self.instantiate_sqlite_table(write_file)
        for x in content:
            self.__debug(f'Inserting {x}')
            self.db_insert(cur, x)
        self.db_commit(cur.connection)
        self.db_close(cur.connection)
