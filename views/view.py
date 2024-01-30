from tkinter import Tk, Menu, messagebox, ttk
import traceback

from .leagues_tab import LeaguesTab

from .stadiums_tab import StadiumsTab

from .nationalities_tab import NationalitiesTab

from .team_names_tab import TeamNamesTab

class View(Tk):
    """
    _summary_
    """
    PAD = 10

    w = 800 # width for the Tk root
    h = 600 # height for the Tk root


    def __init__(self, controller):
        super().__init__()
        
        self.controller = controller
        self.appname ="PES4/WE8 Text Editor"
        self.title(self.appname)
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        self.iconbitmap(default=controller.resource_path("resources/pes_indie.ico"))

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (self.w/2)
        y = (hs/2) - (self.h/2)
        # set the dimensions of the screen 
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        
        self._make_file_menu()
        self._make_tabs()


    def _make_file_menu(self):
        self.my_menu=Menu(self.master)
        self.config(menu=self.my_menu)
        self.file_menu = Menu(self.my_menu, tearoff=0)
        self.edit_menu = Menu(self.my_menu, tearoff=0)
        self.help_menu = Menu(self.my_menu, tearoff=0)

        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open exe", command=lambda : self.controller.on_open_file_menu_click())
        self.file_menu.add_command(label="Save exe", state='disabled',command=lambda : self.controller.on_click_on_save_exe())
        self.file_menu.add_command(label="Exit", command= lambda : self.controller.save_settings_and_close())

        self.my_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_submenu = Menu(self.my_menu, tearoff=0)
        # Dinamically loading game versions as sub menu
        for i, game_config in enumerate(self.controller.my_config.games_config):
            self.edit_submenu.add_command(
                label = game_config,
                command = lambda i = i : self.controller._load_config(i)
            )
        self.edit_menu.add_cascade(label="Game Version", menu=self.edit_submenu)

        self.my_menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Manual", command=None)
        self.help_menu.add_command(label="About", command=None)


    def _make_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.teamnames_tab = TeamNamesTab(master=self.notebook, width=self.w, height=self.h, controller=self.controller)
        self.nationalities_tab = NationalitiesTab(master=self.notebook, width=self.w, height=self.h, controller=self.controller)
        self.stadiums_tab = StadiumsTab(master=self.notebook, width=self.w, height=self.h, controller=self.controller)
        self.leagues_tab = LeaguesTab(master=self.notebook, width=self.w, height=self.h, controller=self.controller)

        self.tabs = [
            self.teamnames_tab, 
            self.nationalities_tab, 
            self.stadiums_tab, 
            self.leagues_tab,
        ]
        
        for tab in self.tabs:
            self.notebook.add(tab, text=tab.tab_name)
        
        self.notebook.pack(side="top", fill="both")

    def report_callback_exception(self, *args):
        err = traceback.format_exception(*args)
        messagebox.showerror(self.appname + " Error Message", " ".join(err))


    def main(self):
        self.mainloop()

