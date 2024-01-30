import struct
from tkinter import filedialog

from .team import Team
from .nationality import Nationality
from .binary_file import BinaryFile

class Model():
    def __init__(self):
        return
    
    def open_file(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        filetypes = [
            ('All files', '*.*'),
        ]

        filename = filedialog.askopenfilename(
            title=f'Select your game executable',
            initialdir='.',
            filetypes=filetypes
        )
        return filename        

    def get_name_offset(self, file_bytes: bytes, offset: int):
        return struct.unpack("<I",file_bytes[offset : offset + 4])[0]

    def get_name(self, file_bytes:bytes, offset:int):
        return file_bytes[offset:].partition(b"\0")[0].decode('utf-8')

    def get_team(self, team_id:int, file_bytes:bytes, offset:int, base_address:int):
        name_offset = self.get_name_offset(file_bytes, offset + 4 + team_id * 20)
        abb_name_offset = self.get_name_offset(file_bytes, offset + 8 + team_id * 20)
        name = self.get_name(file_bytes, name_offset - base_address)
        abb_name = self.get_name(file_bytes, abb_name_offset - base_address)
        return Team(team_id, name, abb_name)

    def get_teams(self, file_bytes: bytes, names_offsets: int, total_teams: int, base_address: int):
        return [
            self.get_team(team_id, file_bytes, names_offsets, base_address)
            for team_id in range(total_teams)
        ]
    
    def get_nationalities(self, file_bytes: bytes, names_offsets: int, total_teams: int, base_address: int):
        return [
            Nationality(
                nt_id,
                file_bytes[
                    self.get_name_offset(file_bytes, names_offsets + 8 + nt_id * 20) - base_address
                    :
                ].partition(b"\0")[0].decode('utf-8'),
                file_bytes[
                    self.get_name_offset(file_bytes, names_offsets + 12 + nt_id * 20) - base_address
                    :
                ].partition(b"\0")[0].decode('utf-8'),
            )
            for nt_id in range(total_teams)
        ]

    def get_stadiums_names(self, file_bytes:bytes, start_offset:int, total_stadiums:int, max_len:int):
        return [
            file_bytes[
                start_offset + stadium_id * max_len
                :
                start_offset + stadium_id * max_len + max_len
            ].partition(b"\0")[0].decode('utf-8')
            for stadium_id in range(total_stadiums)
        ]

    def get_leagues_names(self, file_bytes:bytes, start_offset:int, total:int, max_len:int):
        base_name_len = 20
        record_size = 84
        return [
            file_bytes[
                start_offset + league_id * record_size + base_name_len + 1
                :
                start_offset + league_id * record_size + base_name_len + 1 + max_len 
            ].partition(b"\0")[0].decode('utf-8')
            for league_id in range(total)
        ]

    def set_team_names(self, teams:"list[Team]", base_address:int, start_offset:int, offsets_table:int, data_size:int, file:BinaryFile):
        temp_bytes = bytearray(data_size)
        sum = base_address + start_offset
        sum1 = 0
        for i, team in enumerate(teams):
            name_bytes = team.full_name.encode("utf8","ignore") + bytearray(1)
            abb_bytes = team.abb_name.encode("utf8","ignore") + bytearray(1)
            # we overwrite the offset of the japanese name with the one for english name
            file.set_bytes(offsets_table + i * 20, struct.pack("<I", sum))
            file.set_bytes(offsets_table + 4 + i * 20, struct.pack("<I", sum))
            file.set_bytes(offsets_table + 12 + i * 20, struct.pack("<I", sum))
            sum += len(name_bytes)
            file.set_bytes(offsets_table + 8 + i * 20, struct.pack("<I", sum))
            sum += len(abb_bytes)
            team_name_bytes = name_bytes + abb_bytes
            team_name_bytes_size = len(team_name_bytes)
            temp_bytes[sum1 : sum1 + team_name_bytes_size] = team_name_bytes
            sum1 += team_name_bytes_size
        if len(temp_bytes)>data_size:
            raise ValueError("The buffer for the text data its way too big for the reseved space")
        file.set_bytes(start_offset, temp_bytes)

    def set_nationalities(self, nationalities:"list[Nationality]", base_address:int, start_offset:int, offsets_table:int, data_size:int, file:BinaryFile):
        temp_bytes = bytearray(data_size)
        sum = base_address + start_offset
        sum1 = 0
        for i, nationality in enumerate(nationalities):
            name_bytes = nationality.full_name.encode("utf8","ignore") + bytearray(1)
            abb_bytes = nationality.abb_name.encode("utf8","ignore") + bytearray(1)
            file.set_bytes(offsets_table + 4 + i * 20, struct.pack("<I", sum))
            file.set_bytes(offsets_table + 8 + i * 20, struct.pack("<I", sum))
            file.set_bytes(offsets_table + 16 + i * 20, struct.pack("<I", sum))
            sum += len(name_bytes)
            file.set_bytes(offsets_table + 12 + i * 20, struct.pack("<I", sum))
            sum += len(abb_bytes)
            nationality_bytes = name_bytes + abb_bytes
            nationality_bytes_size = len(nationality_bytes)
            temp_bytes[sum1 : sum1 + nationality_bytes_size] = nationality_bytes
            sum1 += nationality_bytes_size
        if len(temp_bytes)>data_size:
            raise ValueError("The buffer for the text data its way too big for the reseved space")
        file.set_bytes(start_offset, temp_bytes)

    def set_stadiums_names(self, list_of_names:"list[str]", start_offset:int, lenght:int, file:BinaryFile):
        for i, name in enumerate(list_of_names):
            temp_bytes = bytearray(lenght)
            name_bytes = name.encode("utf8","ignore")
            temp_bytes[:len(name_bytes)] = name_bytes
            file.set_bytes(start_offset + i * lenght, temp_bytes)

    def set_leagues_names(self, list_of_names:"list[str]", start_offset:int, lenght:int, file:BinaryFile):
        base_name_len = 20
        record_size = 84
        for i, name in enumerate(list_of_names):
            temp_bytes = bytearray(lenght)
            name_bytes = name.encode("utf8","ignore")
            temp_bytes[:len(name_bytes)] = name_bytes
            file.set_bytes(start_offset + base_name_len + 1 + i * record_size, temp_bytes)

