import tkinter as tk
from static import frames


class Menubar(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        tk.Menu.__init__(self, parent, *args, **kwargs)

        filemenu = tk.Menu(self, tearoff=0)
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Save as...")
        filemenu.add_command(label="Close")

        self.add_cascade(label="File", menu=filemenu)


class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.basic_info_card = frames.BasicInfoCard(self, 'Basic Info')
        self.basic_combat_frame = frames.BasicCombatCard(self, 'Combat')

        self.widgets = [self.basic_info_card, self.basic_combat_frame]

        self.grid_items()

    def grid_items(self):
        for widget in self.widgets:
            widget.grid_items()

        self.basic_info_card.grid(row=0, column=0)
        self.basic_combat_frame.grid(row=0, column=1)

    def save(self):
        for widget in self.widgets:
            widget.save()