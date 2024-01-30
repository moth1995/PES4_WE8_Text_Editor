from tkinter import ttk, Listbox
from views.custom_widget import Entry

class StadiumsTab(ttk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.stadiums_id_lbl = ttk.Label(self,text = "Stadium ID: ")
        self.stadiums_id_box = Entry(self, width=4, state = "readonly")
        self.stadiums_lbl = ttk.Label(self, text = "Stadium Name: ")
        self.stadiums_box = Entry(self, width=40)
        self.stadiums_apply_btn = ttk.Button(
            self, 
            text = "Apply", 
            command=lambda : self.controller.stadiums_apply_btn_action(
                int(self.stadiums_id_box.get()),
                self.stadiums_box.get(),
            )
        )
        self.stadiums_cancel_btn = ttk.Button(self, text = "Cancel", command=None)

        self.stadiums_list_box = Listbox(self, height = 34, width = 50, exportselection = False)
        self.stadiums_list_box_sb = ttk.Scrollbar(self, orient="vertical") 
        self.stadiums_list_box_sb.config(command = self.stadiums_list_box.yview)
        self.stadiums_list_box.config(yscrollcommand = self.stadiums_list_box_sb.set)

        self.stadiums_id_lbl.place(x = 360, y = 20)
        self.stadiums_id_box.place(x = 460, y = 20)
        self.stadiums_lbl.place(x = 360, y = 50)
        self.stadiums_box.place(x = 460, y = 50)
        self.stadiums_apply_btn.place(x = 400, y = 80)
        self.stadiums_cancel_btn.place(x = 480, y = 80)

        self.stadiums_list_box.place(x = 5, y = 20)
        self.stadiums_list_box_sb.place(x = 310, y = 20 , height = 550)

    @property
    def tab_name(self):
        return "Stadiums"

