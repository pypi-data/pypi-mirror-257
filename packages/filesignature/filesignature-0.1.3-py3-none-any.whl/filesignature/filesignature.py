# -*- coding: utf-8 -*-
"""
The purpose of this class is to search the signatures of the files, compare
them and return the information obtained to check that the file in question
corresponds to the extension it has, in short, that it is valid.

The information used is contained in the `file_signatures` file, and is
obtained using the `filesignaturecollectors` package.

* https://github.com/kurotom/filesignaturecollectors


Notes:

ISO-8859-1/latin-1

Fields of data:
    * hex_signature
    * byte_offset
    * file_extentions

Data location:
    * Linux: `~/.config/filesignaturecollectors`
    * Windows: `%APPDATA%\\Roaming\\filesignaturecollectors\\`
    * Mac: `~/Library/Application Support/filesignaturecollectors/`

"""

from filesignaturecollectors.utils.store_data import get_platform
from filesignature.models import MagicNumberData
from filesignature.collector import CollectorData

import mimetypes
import os

from typing import Tuple, Union, List


class FileSignature:
    '''
    Class in charge of searching, extracting and comparing the signatures of
    the files, returning the obtained results.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.ROOT_DIRECTORY = get_platform()
        self.file_signature_path = os.path.join(
                                        self.ROOT_DIRECTORY,
                                        'file_signatures'
                                    )
        self.__check_file_signature_exists()
        self.magicnumbersdata = self.__get_data()
        self.file_seek = None
        self.file_sign_data = {}

    def __check_file_signature_exists(self) -> None:
        if not os.path.exists(self.file_signature_path):
            c = CollectorData()
            c.get(dest='filesignature')

    def __get_data(self) -> list:
        '''
        Load data of `file_signatures` File.
        '''
        result = []
        with open(self.file_signature_path, 'r') as fl:
            data = fl.readlines()
        for item in data[1:]:
            line = item.split('\t')
            magic = MagicNumberData(
                            hex_signature=line[0],
                            byte_offset=line[1],
                            file_extentions=line[2]
                    )
            result.append(magic)
        return result

    def read(
        self,
        file_path: str,
        mode: str = 'rb',
    ) -> bytes:
        '''
        Opens and readlines of the file.

        Return data of file.
        '''
        with open(file_path, mode) as fl:
            return fl.readlines()

    def read_seek(
        self,
        file_path: str,
        byte_offset: str
    ) -> bytes:
        '''
        Opens the file, jumps to the byte offset position and returns the
        rawdata.
        '''
        if byte_offset == 'None' or byte_offset is None:
            byte_offset = 0
        else:
            byte_offset = int(byte_offset)
        file = open(file_path, 'rb')

        file.seek(byte_offset)
        self.file_seek = file
        return file.read()

    def get_filename_extention(
        self,
        file_path: str
    ) -> Tuple[str, str]:
        '''
        Get extention from filename.
        '''
        filename, file_extention = os.path.splitext(file_path)
        return filename, file_extention.replace('.', '').lower()

    def to_close(self) -> None:
        '''
        Close open file.
        '''
        try:
            self.file_seek.close()
        except AttributeError:
            pass

    def get_hex_sign_file(
        self,
        rawdata: bytes,
        index: int = 4
    ) -> str:
        '''
        Transforms byte data into hexadecimal signature, limited by the `index`
        value.
        '''
        hexsign = ''
        for i in rawdata[:index]:
            ahex = hex(i)[2:]
            if ahex.isnumeric():
                ahex = '%02d' % int(ahex)
            hexsign += ahex.upper()
        hex_signs_list = [hexsign[i:i + 2] for i in range(0, len(hexsign), 2)]
        return ' '.join(hex_signs_list)

    def filter_by_extention(
        self,
        file_extention: str,
    ) -> None:
        '''
        Filter Magic Number data using extention.

        Return a list of tuples with matched data.
        '''
        result = []
        for item in self.magicnumbersdata:
            hex_signatures = item.hex_signature
            bytes_offset = item.byte_offset
            file_extentions = item.file_extentions
            if file_extention in file_extentions:
                data = (hex_signatures, bytes_offset, file_extentions)
                result.append(data)
        return result

    def filter_by_hexsign(
        self,
        file_signature: str,
    ) -> None:
        '''
        Filter Magic Number data using hex_sign.

        Return a list of tuples with hex signs matches.
        '''
        result = []
        filesignature_list = file_signature.split(' ')

        for item in self.magicnumbersdata:
            hex_signatures = item.hex_signature
            bytes_offset = item.byte_offset
            file_extentions = item.file_extentions
            # print(file_signature, hex_signatures)

            for hexsign in hex_signatures:
                list_hexsing = hexsign.split(' ')
                pairs_list = list(zip(list_hexsing, filesignature_list))
                resBool = [i[0] == i[1] for i in pairs_list]
                countTrues = resBool.count(True)
                countFalses = resBool.count(False)
                values = countTrues - countFalses
                if values >= 1:
                    data = (hexsign, bytes_offset, file_extentions)
                    result.append(data)

        return result

    def check_bytes_type(
        self,
        raw_data: bytes,
        extention: str = None
    ) -> Union[List[Tuple], Tuple]:
        '''
        Checks the type of the data bytes, optionally (recommended) filters by
        the extent of the data, if not specified, returns all entries that
        match the hexadecimal signature of the raw data.
        '''
        hex_sign_file = self.get_hex_sign_file(
                                rawdata=raw_data
                            )
        data = self.filter_by_hexsign(file_signature=hex_sign_file)
        if extention is not None:
            for item in data:
                hexsign = item[0]
                byteoffset = item[1][0]
                ext_file = item[2][0]
                if extention == ext_file.lower():
                    return (hexsign, byteoffset, ext_file)
        else:
            return data

    def check_file_type(
        self,
        file_path: str,
        get_bool: bool = False
    ) -> Union[dict, bool]:
        '''
        Checks if the file corresponds to the type in which it is stored. If
        `get_bool=True` (`False` - default) returns boolean indicating if the
        file has the correct format.

        Note:
        If you do not find any matching entries, the given file may be
        corrupted, saved in the wrong format, had its extension changed
        manually.
        '''
        file_mimetype = mimetypes.guess_type(file_path)[0]
        filename, file_extention = self.get_filename_extention(
                                        file_path=file_path
                                    )

        filter_extentions = self.filter_by_extention(
                                        file_extention=file_extention
                                    )
        matches = []
        for item in filter_extentions:
            hex_signs_list = item[0]
            byte_offset = item[1]
            # file_extentions = item[2]

            if '+=' in byte_offset[0]:
                file_size = os.path.getsize(file_path)
                byte_offset_every188 = 0
                while byte_offset_every188 < file_size:
                    data_iter = self.iteration_hexsigns(
                            list_hex_signs=hex_signs_list,
                            path_file=file_path,
                            int_byte_offset=byte_offset_every188
                        )
                    if len(data_iter) > 0:
                        matches += data_iter
                        break
                    byte_offset_every188 += 188

            elif '-' in byte_offset[0]:
                data_matches = self.iteration_hexsigns(
                        list_hex_signs=hex_signs_list,
                        path_file=file_path,
                        int_byte_offset=int(byte_offset[0])
                    )
                if data_matches != []:
                    matches += data_matches
            elif len(byte_offset) > 1:
                for byteoffset in byte_offset:
                    data_matches += self.iteration_hexsigns(
                        list_hex_signs=hex_signs_list,
                        path_file=file_path,
                        int_byte_offset=int(byteoffset)
                    )
                    if data_matches != []:
                        matches += data_matches
            else:
                data_matches = self.iteration_hexsigns(
                        list_hex_signs=hex_signs_list,
                        path_file=file_path,
                        int_byte_offset=int(byte_offset[0])
                    )
                if data_matches != []:
                    matches += data_matches

        self.file_sign_data = {
            'filename': filename,
            'file_extention': file_extention,
            'mimetype': file_mimetype,
            'file_signature': matches != []
        }
        if get_bool:
            return self.file_has_hexsignature()
        else:
            return self.file_sign_data

    def iteration_hexsigns(
        self,
        list_hex_signs: list,
        path_file: str,
        int_byte_offset: int
    ) -> list:
        '''
        Iterates the hexadecimal signatures of the matching entries, compared
        to the hexadecimal signature of the given file.

        Return a list of all matches.
        '''
        matches = []
        for hexsign in list_hex_signs:
            index_rawData = len(hexsign.replace(' ', '')) // 2
            rawdata = self.read_seek(
                                file_path=path_file,
                                byte_offset=int_byte_offset
                            )

            hex_sign_file = self.get_hex_sign_file(
                                    rawdata=rawdata,
                                    index=index_rawData
                                )
            self.to_close()
            # print(hexsign, '---', hex_sign_file)
            if hexsign == hex_sign_file:
                if hexsign not in matches:
                    matches.append(hexsign)
        return matches

    def file_has_hexsignature(
        self
    ) -> dict:
        '''
        Returns results of the analysis of the given file.
        '''
        return self.file_sign_data['file_signature']

    def search(
        self,
        extention: str,
        only_hex: bool = False
    ) -> dict:
        hexsigns_list = []
        byteoffet_list = []
        extentions_list = []
        for item in self.magicnumbersdata:
            hexsigns = item.hex_signature
            byteoffet = item.byte_offset
            extentions = item.file_extentions
            if extention.lower() in extentions:
                hexsigns_list += hexsigns
                byteoffet_list += byteoffet
                extentions_list += extentions
        if only_hex:
            return {'hexsigns': list(set(hexsigns_list))}
        else:
            return {
                'hexsigns': list(set(hexsigns_list)),
                'byteoffet': list(set(byteoffet_list)),
                'extentions': list(set(extentions_list)),
            }
