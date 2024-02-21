# -*- coding: utf-8 -*-
"""
Models
"""

from typing import TypeVar, Union, List
from uuid import uuid1

FileMagicDataInstace = TypeVar('FileMagicDataInstace')
uuid4HexStr = TypeVar('uuid4HexStr')


class FileMagicData:
    index = 0

    def __init__(
        self,
        id: uuid4HexStr,
        hex_signature: Union[str, List[str]] = None,
        file_extentions: Union[str, List[str]] = None,
        ascii_signature: Union[str, List[str]] = None,
        file_description: Union[str, List[str]] = None,
        byte_offset: Union[int, str, List[str]] = None,
        notes: str = None,
        notes_hex_signs: str = None
    ):
        self.idx = None
        self.id = self.objID(id_hash=id)
        self.hex_signature = hex_signature
        self.file_extentions = file_extentions
        self.ascii_signature = ascii_signature
        self.file_description = file_description
        self.byte_offset = byte_offset
        self.notes = notes
        self.notes_hex_signs = notes_hex_signs

    def objID(
        self,
        id_hash: str
    ) -> str:
        if id_hash is None:
            return uuid1().hex
        else:
            return id_hash

    def compare(
        self,
        obj: FileMagicDataInstace
    ) -> bool:
        sign = obj.hex_signature.split('|')
        signs_bool = [i_sign in self.hex_signature for i_sign in sign]
        return any(signs_bool)

    def join_items(
        self,
        data: list,
        lower: bool = False
    ) -> Union[list | None]:
        if type(data) is list:
            black_list = [
                    'empty archive',
                    'spanned archive',
                    'little-endian',
                    'big-endian',
                ]
            new_data = []
            for item in data:
                if item not in black_list:
                    if lower:
                        new_data.append(item.lower().strip())
                    else:
                        new_data.append(item.strip())
            return '|'.join(new_data)
        else:
            if type(data) is None:
                return '%d' % data.lower()
            else:
                return '0'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'hex_signature': self.join_items(data=self.hex_signature),
            'byte_offset': self.join_items(self.byte_offset),
            'ascii_signature': self.join_items(self.ascii_signature),
            'file_extentions': self.join_items(
                                        self.file_extentions,
                                        lower=True
                                    ),
            'file_description': self.file_description,
            'notes': self.notes,
            'notes_hex_signs': self.join_items(self.notes_hex_signs)
        }

    def __str__(self) -> str:
        return '<[%s, %s, %s]>' % (
                    self.id,
                    self.file_extentions,
                    self.hex_signature,
                )
