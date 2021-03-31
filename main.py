import tkinter as tk
import database as db
import character as ch
import frontend as fe


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.main_window = fe.MainWindow(self.root)
        self.menu_bar = fe.Menubar(self.root)

        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.root.config(menu=self.menu_bar)

    def main(self):
        self.main_window.grid(row=0, column=0)
        self.root.mainloop()

    def on_exit(self):
        self.main_window.save()
        ch.character.misc_items.save()
        self.root.destroy()


if __name__ == "__main__":
    # db.init_db()
    app = App()
    app.main()
