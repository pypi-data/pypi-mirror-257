"""
Provides a standard file type class object
"""
from dataclasses import dataclass

import json
import jsonpickle

@dataclass
class File():
    """Represents any kind of file, extend to provide file type specific 
    properties
    """

    path:str
    file_name:str
    file_type:str
    mtime:int

    def __str__(self) -> str:
        return jsonpickle.encode(self)
    def __repr__(self) -> str:
        return self.__str__()
    def to_json(self) -> str:
        """Returns the json string representation of this object

        Returns:
            str: json string
        """
        return json.dumps(self, default=lambda self: self.__dict__)
