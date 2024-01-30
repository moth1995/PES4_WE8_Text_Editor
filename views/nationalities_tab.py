from tkinter import ttk, Listbox
from views.custom_widget import Entry

class NationalitiesTab(ttk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.nationalities_id_lbl = ttk.Label(self,text = "Nationality ID: ")
        self.nationalities_id_box = Entry(self, width=4, state = "readonly")
        self.nationalities_abb_lbl = ttk.Label(self, text = "Short Name: ")
        self.nationalities_abb_box = Entry(self, width=40)
        self.nationalities_lbl = ttk.Label(self, text = "Full Name: ")
        self.nationalities_box = Entry(self, width=40)

        self.nationalities_apply_btn = ttk.Button(
            self, 
            text = "Apply", 
            command=lambda : self.controller.nationality_apply_btn_action(
                int(self.nationalities_id_box.get()),
                self.nationalities_box.get(),
                self.nationalities_abb_box.get(),
            )
        )
        self.nationalities_cancel_btn = ttk.Button(self, text = "Cancel", command=None)

        self.nationalities_list_box = Listbox(self, height = 34, width = 50, exportselection = False)
        self.nationalities_list_box_sb = ttk.Scrollbar(self, orient="vertical") 
        self.nationalities_list_box_sb.config(command = self.nationalities_list_box.yview)
        self.nationalities_list_box.config(yscrollcommand = self.nationalities_list_box_sb.set)

        self.nationalities_id_lbl.place(x = 360, y = 20)
        self.nationalities_id_box.place(x = 440, y = 20)
        self.nationalities_abb_lbl.place(x = 360, y = 50)
        self.nationalities_abb_box.place(x = 440, y = 50)
        self.nationalities_lbl.place(x = 360, y = 80)
        self.nationalities_box.place(x = 440, y = 80)

        self.nationalities_apply_btn.place(x = 400, y = 110)
        self.nationalities_cancel_btn.place(x = 480, y = 110)

        self.nationalities_list_box.place(x = 5, y = 20)
        self.nationalities_list_box_sb.place(x = 310, y = 20 , height = 550)

    @property
    def tab_name(self):
        return "Nationalities"

