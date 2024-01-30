from tkinter import ttk, Listbox
from views.custom_widget import Entry

class TeamNamesTab(ttk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.teamnames_id_lbl = ttk.Label(self,text = "Team ID: ")
        self.teamnames_id_box = Entry(self, width=4, state = "readonly")
        self.teamnames_abb_lbl = ttk.Label(self, text = "Short Name: ")
        self.teamnames_abb_box = Entry(self, width=40)
        self.teamnames_lbl = ttk.Label(self, text = "Full Name: ")
        self.teamnames_box = Entry(self, width=40)

        self.teamnames_apply_btn = ttk.Button(
            self, 
            text = "Apply", 
            command=lambda : self.controller.teams_apply_btn_action(
                int(self.teamnames_id_box.get()),
                self.teamnames_box.get(),
                self.teamnames_abb_box.get(),
            )
        )
        self.teamnames_cancel_btn = ttk.Button(self, text = "Cancel",)

        self.teamnames_list_box = Listbox(self, height = 34, width = 50, exportselection = False)
        self.teamnames_list_box_sb = ttk.Scrollbar(self, orient="vertical") 
        self.teamnames_list_box_sb.config(command = self.teamnames_list_box.yview)
        self.teamnames_list_box.config(yscrollcommand = self.teamnames_list_box_sb.set)

        self.teamnames_id_lbl.place(x = 360, y = 20)
        self.teamnames_id_box.place(x = 440, y = 20)
        self.teamnames_abb_lbl.place(x = 360, y = 50)
        self.teamnames_abb_box.place(x = 440, y = 50)
        self.teamnames_lbl.place(x = 360, y = 80)
        self.teamnames_box.place(x = 440, y = 80)

        self.teamnames_apply_btn.place(x = 400, y = 110)
        self.teamnames_cancel_btn.place(x = 480, y = 110)

        self.teamnames_list_box.place(x = 5, y = 20)
        self.teamnames_list_box_sb.place(x = 310, y = 20 , height = 550)

    @property
    def tab_name(self):
        return "Team Names"

