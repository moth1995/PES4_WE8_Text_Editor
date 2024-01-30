from tkinter import ttk, Listbox
from views.custom_widget import Entry

class LeaguesTab(ttk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.league_id_lbl = ttk.Label(self,text = "League ID: ")
        self.league_id_box = Entry(self, width=4, state = "readonly")
        self.league_lbl = ttk.Label(self, text = "League Name: ")
        self.league_box = Entry(self, width=40)
        self.league_apply_btn = ttk.Button(
            self, 
            text = "Apply", 
            command= lambda : self.controller.leagues_apply_btn_action(
                int(self.league_id_box.get()),
                self.league_box.get(),
            )
        )
        self.league_cancel_btn = ttk.Button(self, text = "Cancel", command=None)

        self.league_list_box = Listbox(self, height = 34, width = 50, exportselection = False)
        self.league_list_box_sb = ttk.Scrollbar(self, orient="vertical") 
        self.league_list_box_sb.config(command = self.league_list_box.yview)
        self.league_list_box.config(yscrollcommand = self.league_list_box_sb.set)

        self.league_id_lbl.place(x = 360, y = 20)
        self.league_id_box.place(x = 460, y = 20)
        self.league_lbl.place(x = 360, y = 50)
        self.league_box.place(x = 460, y = 50)
        self.league_apply_btn.place(x = 400, y = 80)
        self.league_cancel_btn.place(x = 480, y = 80)

        self.league_list_box.place(x = 5, y = 20)
        self.league_list_box_sb.place(x = 310, y = 20 , height = 550)

    @property
    def tab_name(self):
        return "Leagues"

