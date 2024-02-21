# -*- coding: utf-8 -*-
"""
"""


class MagicNumberData:

    def __init__(
        self,
        hex_signature: str = None,
        byte_offset: str = None,
        file_extentions: str = None
    ):
        self.hex_signature = self.to_list(data=hex_signature)
        self.byte_offset = self.to_list(data=byte_offset)
        self.file_extentions = self.to_list(data=file_extentions)

    def to_list(
        self,
        data: str
    ) -> list:
        return data.strip().split('|')

    def __str__(self) -> str:
        return '%s %s' % (self.file_extentions, self.hex_signature)
