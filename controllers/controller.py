from pathlib import Path
from tkinter import Listbox, messagebox, ttk
from models.binary_file import BinaryFile
from models.config import Config
from models.model import Model
from views.view import View
import yaml, os, sys

class Controller():
    def __init__(self):
        self.my_config = Config()
        self.model = Model()
        self.view = View(self)
        self.executable = BinaryFile("")
        self._load_settings()
        self.leagues_max_len = 61
        self.teams = []
        self.nationalities = []
        self.stadiums_list = []
        self.leagues_names_list = []
        
        self.view.teamnames_tab.teamnames_list_box.bind(
            '<<ListboxSelect>>', 
            lambda _ : self.tn_nt_data_to_entry(
                self.view.teamnames_tab.teamnames_list_box, 
                self.view.teamnames_tab.teamnames_box,
                self.view.teamnames_tab.teamnames_abb_box,
                self.view.teamnames_tab.teamnames_id_box,
                [] if self.teams ==[] else [team.full_name for team in self.teams],
                [] if self.teams ==[] else [team.abb_name for team in self.teams],
            )
        )
        
        self.view.nationalities_tab.nationalities_list_box.bind(
            '<<ListboxSelect>>', 
            lambda _ : self.tn_nt_data_to_entry(
                self.view.nationalities_tab.nationalities_list_box, 
                self.view.nationalities_tab.nationalities_box,
                self.view.nationalities_tab.nationalities_abb_box,
                self.view.nationalities_tab.nationalities_id_box,
                [] if self.nationalities ==[] else [nationality.full_name for nationality in self.nationalities],
                [] if self.nationalities ==[] else [nationality.abb_name for nationality in self.nationalities],
            )
        )

        self.view.stadiums_tab.stadiums_list_box.bind(
            '<<ListboxSelect>>', 
            lambda _ : self.st_lg_data_to_entry(
                self.view.stadiums_tab.stadiums_list_box, 
                self.view.stadiums_tab.stadiums_box,
                self.view.stadiums_tab.stadiums_id_box,
                self.stadiums_list,
            )
        )

        self.view.leagues_tab.league_list_box.bind(
            '<<ListboxSelect>>', 
            lambda _ : self.st_lg_data_to_entry(
                self.view.leagues_tab.league_list_box, 
                self.view.leagues_tab.league_box,
                self.view.leagues_tab.league_id_box,
                self.leagues_names_list,
            )
        )

    def _load_settings(self):
        load_defaults = False
        try:
            with open(str(Path().absolute()) + "/settings.yaml") as stream:
                self.settings_file = yaml.safe_load(stream)
                self._load_config(self.my_config.filelist.index(self.settings_file.get('Last Config File Used')))
        except Exception as e:
            load_defaults = True
            messagebox.showinfo(title=self.view.appname, message=f"No setting file found\nLoading first config file")
        if load_defaults:
            try:
                self._load_config(0)
            except Exception as e:
                messagebox.showerror(title=self.view.appname, message=f"No config files found code error {e}")
                self.view.destroy()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    def save_settings_and_close(self):
        settings_file_name = str(Path().absolute()) + "/settings.yaml"
        
        dict_file = {
            'Last Config File Used' : self.my_config.file_location,
        }

        settings_file = open(settings_file_name, "w")
        yaml.dump(dict_file, settings_file)
        settings_file.close()
        self.view.destroy()


    def _load_config(self, idx):
        self.my_config.load_config(idx)
        self.view.appname = "PES4/WE8 Text Editor " + self.my_config.file["Gui"]["Game Name"]
        self.view.title(self.view.appname)

        # Game data
        self.base_address = self.my_config.file["Game Data"]["Base Address"]
        self.total_stadiums = self.my_config.file["Game Data"]["Total Stadiums"]
        self.stadiums_max_len = self.my_config.file["Game Data"]["Stadium Name Lenght"]
        self.total_leagues = self.my_config.file["Game Data"]["Total Leagues"]
        self.total_teams = self.my_config.file["Game Data"]["Total Teams"]
        self.total_nationalities = self.my_config.file["Game Data"]["Total Nationalities"]        

        # EXE offsets

        self.names_offsets_table = self.my_config.file["Offsets"]["Teams Offsets Table"]
        self.teams_names_data_offset = self.my_config.file["Offsets"]["Teams Text Data Offset"]
        self.teams_names_text_size = self.my_config.file["Offsets"]["Teams Text Data Size"]

        self.nationalities_offsets_table = self.my_config.file["Offsets"]["Nationalities Offsets Table"]
        self.nationalities_data_offset = self.my_config.file["Offsets"]["Nationalities Text Data Offset"]
        self.nationalities_text_size = self.my_config.file["Offsets"]["Nationalities Text Data Size"]

        self.stadiums_offsets_table = self.my_config.file["Offsets"]["Stadiums Offsets Table 1"]
        self.stadiums_offsets_table2 = self.my_config.file["Offsets"]["Stadiums Offsets Table 2"]

        self.leagues_offsets_table = self.my_config.file["Offsets"]["Leagues Offsets Table 1"]
        self.leagues_offsets_table2 = self.my_config.file["Offsets"]["Leagues Offsets Table 2"]


    def main(self):
        self.view.main()

    def on_open_file_menu_click(self):
        file_path = (self.model.open_file())
        if file_path != "":
            self.executable.filename = file_path
        if (
            self.executable.size > 0 and 
            self.names_offsets_table != 0 and 
            self.nationalities_offsets_table != 0 and
            self.stadiums_offsets_table != 0 and 
            self.stadiums_offsets_table2 != 0 and 
            self.leagues_offsets_table != 0 and 
            self.leagues_offsets_table2 != 0
        ):
            # loading teamnames into listbox
            self.teams = self.model.get_teams(self.executable.file_bytes, self.names_offsets_table, self.total_teams, self.base_address)
            self.view.teamnames_tab.teamnames_list_box.delete(0, "end")
            self.view.teamnames_tab.teamnames_list_box.insert("end", *[team.full_name for team in self.teams])
            
            # loading nationalities into listbox
            self.nationalities = self.model.get_nationalities(self.executable.file_bytes, self.nationalities_offsets_table, self.total_nationalities, self.base_address)

            self.view.nationalities_tab.nationalities_list_box.delete(0, "end")
            self.view.nationalities_tab.nationalities_list_box.insert("end", *[nationality.full_name for nationality in self.nationalities])

            # loading stadiums into listbox
            
            self.stadiums_list = self.model.get_stadiums_names(self.executable.file_bytes, self.stadiums_offsets_table, self.total_stadiums, self.stadiums_max_len)
            
            self.view.stadiums_tab.stadiums_list_box.delete(0, "end")
            self.view.stadiums_tab.stadiums_list_box.insert("end", *self.stadiums_list)
            
            # loading leagues into listbox
            
            self.leagues_names_list = self.model.get_leagues_names(self.executable.file_bytes, self.leagues_offsets_table, self.total_leagues, self.leagues_max_len)
            
            self.view.leagues_tab.league_list_box.delete(0, "end")
            self.view.leagues_tab.league_list_box.insert("end", *self.leagues_names_list)

            self.view.file_menu.entryconfig("Save exe", state='normal')


    def tn_nt_data_to_entry(self, listbox: Listbox, full_name: ttk.Entry, abb: ttk.Entry, id_entry: ttk.Entry, fullnames_list:list, short_names_list: list):
        if listbox.curselection() == ():
            return

        idx = listbox.curselection()[0]
        
        full_name.delete(0,'end')
        full_name.insert(0, fullnames_list[idx])
        
        abb.delete(0,'end')
        abb.insert(0, short_names_list[idx])
        
        id_entry.configure(state='normal')
        id_entry.delete(0,'end')
        id_entry.insert(0, idx)
        id_entry.configure(state='readonly')

    def st_lg_data_to_entry(self, listbox: Listbox, full_name: ttk.Entry, id_entry: ttk.Entry, fullnames_list:list):
        if listbox.curselection() == ():
            return
        idx = listbox.curselection()[0]
        
        full_name.delete(0,'end')
        full_name.insert(0, fullnames_list[idx])
                
        id_entry.configure(state='normal')
        id_entry.delete(0,'end')
        id_entry.insert(0, idx)
        id_entry.configure(state='readonly')

    def teams_apply_btn_action(self, idx: int, name:str, abb:str):
        self.teams[idx].full_name = name
        self.teams[idx].abb_name = abb
        self.view.teamnames_tab.teamnames_list_box.delete(idx,idx)
        self.view.teamnames_tab.teamnames_list_box.insert(idx, self.teams[idx].full_name)
        self.view.teamnames_tab.teamnames_list_box.select_set(idx)

    def nationality_apply_btn_action(self, idx: int, name:str, abb:str):
        self.nationalities[idx].full_name = name
        self.nationalities[idx].abb_name = abb
        self.view.nationalities_tab.nationalities_list_box.delete(idx,idx)
        self.view.nationalities_tab.nationalities_list_box.insert(idx, self.nationalities[idx].full_name)
        self.view.nationalities_tab.nationalities_list_box.select_set(idx)

    def stadiums_apply_btn_action(self, idx: int, name:str):
        if len(name)>= self.stadiums_max_len:
            messagebox.showerror(title = self.view.appname, message = f"Stadium name can be only {self.stadiums_max_len - 1} long")
            return
        self.stadiums_list[idx] = name
        self.view.stadiums_tab.stadiums_list_box.delete(idx,idx)
        self.view.stadiums_tab.stadiums_list_box.insert(idx, self.stadiums_list[idx])
        self.view.stadiums_tab.stadiums_list_box.select_set(idx)

    def leagues_apply_btn_action(self, idx: int, name:str):
        if len(name)>= self.leagues_max_len:
            messagebox.showerror(title = self.view.appname, message = f"League name can be only {self.leagues_max_len - 1} long")
            return
        self.leagues_names_list[idx] = name
        self.view.leagues_tab.league_list_box.delete(idx,idx)
        self.view.leagues_tab.league_list_box.insert(idx, self.leagues_names_list[idx])
        self.view.leagues_tab.league_list_box.select_set(idx)

    def on_click_on_save_exe(self):
        try:
            self.model.set_team_names(
                self.teams, 
                self.base_address, 
                self.teams_names_data_offset,
                self.names_offsets_table, 
                self.teams_names_text_size, 
                self.executable
            )
            self.model.set_nationalities(
                self.nationalities, 
                self.base_address, 
                self.nationalities_data_offset,
                self.nationalities_offsets_table, 
                self.nationalities_text_size, 
                self.executable
            )
            self.model.set_stadiums_names(self.stadiums_list, self.stadiums_offsets_table,self.stadiums_max_len, self.executable)
            self.model.set_stadiums_names(self.stadiums_list, self.stadiums_offsets_table2,self.stadiums_max_len, self.executable)
            self.model.set_leagues_names(self.leagues_names_list, self.leagues_offsets_table,self.leagues_max_len, self.executable)
            self.model.set_leagues_names(self.leagues_names_list, self.leagues_offsets_table2,self.leagues_max_len, self.executable)

            messagebox.showinfo(title = self.view.appname, message = f"All changes saved at {self.executable.filename}")
        except Exception as e:
            messagebox.showinfo(title = self.view.appname, message = f"Error while saving, error type: {e}")

if __name__ == "__main__":
    text_editor = Controller()
    text_editor.main()
