# -*- coding: utf-8 -*-
"""
Class to save data into a file with format:

The file generated have 5 columns and separates using tabulation.

Columns:
    * `hex_signature`
    * `file_extentions`
    * `ascii_signature`
    * `file_description`
    * `byte_offset`

The file is saved with the name `file_signatures` default, and you can give
another filename if you wish.

Notes:
* Byte Offset
    * '-512' => last 512 bytes.
    * '+=188' =>  every 188th bytes.
"""

from filesignaturecollectors.utils.store_data import get_platform

import os
from typing import Tuple, TypeVar


FileMagicDataDict = TypeVar('FileMagicDataDict')


class ToFile:
    def __init__(
        self,
        filename: str = 'file_signatures'
    ):
        self.ROOT_DIRECTORY = get_platform()
        self.filename = self.__buil_path(filename=filename)

    def __buil_path(
        self,
        filename: str
    ) -> str:
        return os.path.join(self.ROOT_DIRECTORY, filename)

    def to_file(
        self,
        tupleFileMagicDict: Tuple[FileMagicDataDict],
        path: str = '.'
    ) -> None:
        data_string = ''

        data_string += '%s\t%s\t%s\n' % (
                    'hex_signature',
                    'byte_offset',
                    'file_extentions'
                )

        for item in tupleFileMagicDict:
            hex_signature = item['hex_signature']
            byte_offset = item['byte_offset']
            file_extentions = item['file_extentions']

            if file_extentions is None:
                file_extentions = 'null'

            s = '%s\t%s\t%s' % (
                            hex_signature,
                            byte_offset,
                            file_extentions
                        )
            data_string += s.strip() + '\n'

        dest_path = os.path.join(path, self.filename)
        self.write(file_name=dest_path, data=data_string)

    def write(
        self,
        file_name: str,
        data: str
    ) -> None:
        with open(file_name, 'w') as file:
            file.write(data)
