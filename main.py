import tkinter as tk
import database as db
import character as ch
import frontend as fe


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.main_window = fe.MainWindow(self.root)
        self.create_menu_bar()

        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    def create_menu_bar(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Character")
        file_menu.add_command(label="Open Character")
        file_menu.add_command(label="Save Changes", command=self.save)
        file_menu.add_command(label="Close", command=self.on_exit)

        menu_bar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menu_bar)

    def save(self):
        self.main_window.save()
        ch.character.misc_items.save()

    def main(self):
        self.main_window.grid(row=0, column=0)
        self.root.mainloop()

    def on_exit(self):
        self.save()
        self.root.destroy()


if __name__ == "__main__":
    # db.init_db()
    app = App()
    app.main()
