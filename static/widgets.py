import tkinter as tk
from abc import ABC, abstractmethod
from character import character
from static.settings import *
import static_functions as sf


class CustomHolderFrame(ABC, tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.widgets = []

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def grid_items(self):
        pass


class TopStatFrame(CustomHolderFrame):
    def __init__(self, parent, attr, label_text, *args, **kwargs):
        CustomHolderFrame.__init__(self, parent, *args, **kwargs)

        self.char_attr = attr

        self.entry = NumberEntry(self)
        self.label = tk.Label(self, text=label_text)

        self.set_entry()

    def set_entry(self):
        self.entry.insert(0, character.get_single_attr(self.char_attr))

    def grid_items(self):
        self.label.grid(row=1, column=0)
        self.entry.grid(row=0, column=0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def save(self):
        character.save_single_attr(self.char_attr, self.entry.get())


class LabelEntryPair(CustomHolderFrame):
    def __init__(self, parent, attr, entry_type, label_text, style=None, *args, **kwargs):
        CustomHolderFrame.__init__(self, parent, *args, **kwargs)

        self.entry_type = entry_type
        self.entry = entry_type(self)
        self.label = tk.Label(self, text=label_text)
        self.mod_label = None
        self.char_attr = attr
        self.style = style

        # parent.widgets.append(self)

        self.set_style()
        self.set_entry()

    def grid_items(self):
        if self.style == 'top combat':
            self.label.grid(row=1, column=0)
            self.entry.grid(row=0, column=0)

        elif self.style == 'textbox':
            self.entry.grid(row=0, column=0)

        else:
            self.label.grid(row=0, column=0)
            self.entry.grid(row=0, column=1)

            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)

        self.grid_mod()

    def set_style(self):
        if self.style == 'top combat':
            self.config(borderwidth=1, relief=tk.GROOVE)
            self.label.config(font=(None, 17))

    def set_entry(self, value=''):
        self.entry.insert(0, character.get_single_attr(self.char_attr))

    def set_label(self, label_text):
        self.label.config(text=label_text)

    def add_mod(self):
        self.mod_label = ModLabel(self, self.char_attr)

    def grid_mod(self):
        if self.mod_label:
            self.mod_label.set_label()
            self.mod_label.grid(row=0, column=2)

            self.columnconfigure(2, weight=1)

    def save(self):
        character.save_single_attr(self.char_attr, self.entry.get())


class CheckLabelPair(CustomHolderFrame):
    def __init__(self, parent, attr1, attr2, label_text, *args, **kwargs):
        CustomHolderFrame.__init__(self, parent, *args, **kwargs)

        self.char_attr = attr1
        self.prof_attr = attr2
        self.var = tk.IntVar()
        self.prof = False

        self.check_proficiency()

        self.check = CustomCheckbutton(self, variable=self.var, text=label_text)
        self.mod_label = ModLabel(self, ability=self.char_attr, prof=self.prof)
        self.mod_label.set_label()

    def check_proficiency(self):
        prof = character.get_single_attr(self.prof_attr)
        if prof == 1:
            self.var.set(1)
            self.prof = True

    def grid_items(self):
        self.check.grid(row=0, column=0)
        self.mod_label.grid(row=0, column=1)

    def save(self):
        character.save_single_attr(self.prof_attr, self.var.get())


class CustomLabel(ABC, tk.Label):
    def __init__(self, parent, *args, **kwargs):
        tk.Label.__init__(self, parent, *args, **kwargs)


class ModLabel(CustomLabel):
    def __init__(self, parent, ability, prof=False, *args, **kwargs):
        CustomLabel.__init__(self, parent, *args, **kwargs)

        self.ability_attr = ability
        self.prof = prof

    def calculate_mod(self):
        score = character.get_single_attr(self.ability_attr)
        mod = sf.calculate_mod(score)
        return self.check_proficiency(mod)

    def check_proficiency(self, mod):
        if self.prof:
            mod += character.get_single_attr('proficiency')
            return mod
        return mod

    def set_label(self):
        self.config(text=str(self.calculate_mod()))


class CustomEntry(ABC, tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent, *args, **kwargs)

    @abstractmethod
    def check_entry_type(self):
        pass

    @abstractmethod
    def check_entry_len(self):
        pass


class NumberEntry(CustomEntry):
    def __init__(self, parent, *args, **kwargs):
        CustomEntry.__init__(self, parent, *args, **kwargs)

        self.config(width=4, justify=tk.CENTER)

    def check_entry_type(self):
        txt = self.get()
        return txt.isnumeric()

    def check_entry_len(self):
        if len(self.get()) > 4:
            return 'Error, too many digits'


class TextEntry(CustomEntry):
    def __init__(self, parent, *args, **kwargs):
        CustomEntry.__init__(self, parent, *args, **kwargs)

        self.config(width=15, justify=tk.CENTER)

    def check_entry_type(self):
        return True

    def check_entry_len(self):
        if len(self.get()) > 15:
            return 'Error, too long'

    def get_entry(self):
        return self.get()

    def reset(self):
        self.delete(0, tk.END)


class CustomCheckbutton(tk.Checkbutton):
    def __init__(self, parent, *args, **kwargs):
        tk.Checkbutton.__init__(self, parent, *args, **kwargs)


class CustomTextbox(tk.Text):
    def __init__(self, parent, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        self.config(width=50, height=13, wrap=tk.WORD)

    def get_entry(self):
        return self.get('1.0', 'end-1c')

    def reset(self):
        self.delete(1.0, tk.END)


class MiscItemPair(LabelEntryPair):

    def set_entry(self, value=''):
        self.entry.reset()
        self.entry.insert(tk.END, value)

    def get_entry(self):
        return self.entry.get_entry()

    def reset(self):
        self.entry.reset()

    def save(self):
        pass


class CustomButton(ABC, tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)

    @abstractmethod
    def grid_items(self):
        pass

    @abstractmethod
    def save(self):
        pass


class MiscButton(CustomButton):
    def __init__(self, parent, *args, **kwargs):
        CustomButton.__init__(self, parent, *args, **kwargs)

    def grid_items(self):
        pass

    def save(self):
        pass


class CustomListbox(ABC, tk.Listbox):
    def __init__(self, parent, *args, **kwargs):
        tk.Listbox.__init__(self, parent, *args, **kwargs)

    def set_list(self, item_name_list):
        for name in reversed(item_name_list):
            self.insert(0, name)

    def get_selection(self):
        return self.get(self.curselection()[0])

    def clear(self):
        self.delete(0, 'end')

    def grid_items(self):
        pass

    def save(self):
        pass


class MiscListbox(CustomListbox):
    def __init__(self, parent, *args, **kwargs):
        CustomListbox.__init__(self, parent, *args, **kwargs)
        self.config(width=20, height=12, font=(None, 14))

        self.bind("<<ListboxSelect>>", self.open_item)

    def change_list(self, list_type):
        self.clear()
        self.set_list(item_name_list=character.misc_type_list(list_type))

    def open_item(self, evt=None):
        pass

    def grid_items(self):
        pass

    def save(self):
        pass


class MiscItemsSelection(CustomHolderFrame):
    def __init__(self, parent, attr, label_text, *args, **kwargs):
        CustomHolderFrame.__init__(self, parent, *args, **kwargs)

        self.name_pair = MiscItemPair(self, label_text='Name', attr='name', entry_type=TextEntry)
        self.desc_pair = MiscItemPair(self, label_text='Description', attr='description',
                                      entry_type=CustomTextbox, style='textbox')
        self.delete_btn = MiscButton(self, text='Delete', command=self.delete)
        self.save_btn = MiscButton(self, text='Save', command=self.save)

        self.type_drop = None
        self.list_box = MiscListbox(self)
        self.list_box.bind("<<ListboxSelect>>", self.load_item)

        self.item = None
        self.list_type = None

    # loads an item from character.misc_items by taking the selection from the listbox
    # then clears the stat block for the item, and replaces it with appropriate info
    def load_item(self, evt=None):
        selection = self.list_box.get_selection()
        self.item = character.misc_items.get_item(selection)
        self.name_pair.set_entry(self.item['name'])
        self.desc_pair.set_entry(self.item['description'])

    def grid_items(self):
        self.name_pair.grid_items()
        self.desc_pair.grid_items()

        self.name_pair.grid(row=1, column=1, sticky=tk.W)
        self.save_btn.grid(row=1, column=2)
        self.delete_btn.grid(row=1, column=3)
        self.desc_pair.grid(row=2, column=1, sticky=tk.E, columnspan=3)
        self.list_box.grid(row=1, column=0, sticky=tk.E, rowspan=2)

    # changes list type, loads the new list, and then loads the first item of the list by default
    def change_list(self, list_type):
        self.list_type = list_type
        self.load_list()
        self.load_default()

    # clears listbox and then replaces it with a refreshed version with current list type
    def load_list(self):
        self.list_box.clear()
        self.list_box.set_list(item_name_list=character.misc_type_list(self.list_type))

    # chooses the first item in list and displays it
    def load_default(self):
        self.list_box.select_set(0)  # This only sets focus on the first item.
        self.list_box.event_generate("<<ListboxSelect>>")

    def delete(self):
        character.misc_items.delete(self.item['id'])
        self.load_list()

    def save(self):
        if self.item:
            self.item['name'] = self.name_pair.get_entry()
            self.item['description'] = self.desc_pair.get_entry()
            character.misc_items.update(self.item)
            self.load_list()


class AddItem(CustomHolderFrame):
    def __init__(self, parent, attr, label_text, *args, **kwargs):
        CustomHolderFrame.__init__(self, parent, *args, **kwargs)

        self.name_pair = MiscItemPair(self, label_text='Name', attr='name', entry_type=TextEntry)
        self.desc_pair = MiscItemPair(self, label_text='Description', attr='description',
                                      entry_type=CustomTextbox, style='textbox')
        self.add_button = MiscButton(self, text='Save Item', command=self.add_item)

        self.options = ['personality', 'ideals', 'bonds', 'flaws']
        self.drop_var = tk.StringVar()
        self.drop_var.set("personality") # default choice
        self.drop_menu = tk.OptionMenu(self, self.drop_var, *self.options)

    def add_item(self):
        character.misc_items.add_item(self.name_pair.get_entry(), self.desc_pair.get_entry(), self.drop_var.get())
        self.reset()

    def grid_items(self):
        self.name_pair.grid_items()
        self.desc_pair.grid_items()

        self.name_pair.grid(row=1, column=1, sticky=tk.W)
        self.desc_pair.grid(row=2, column=1, sticky=tk.E, columnspan=3)
        self.add_button.grid(row=1, column=3, sticky=tk.E)
        self.drop_menu.grid(row=1, column=2, sticky=tk.E)

    def reset(self):
        self.name_pair.reset()
        self.desc_pair.reset()
        self.drop_var.set("personality")

    def save(self):
        pass


class MiscItemsMenu(CustomHolderFrame):
    def __init__(self, parent, attr, label_text, *args, **kwargs):
        CustomHolderFrame.__init__(self, parent, *args, **kwargs)
    # I need an object where the buttons can interact with the list box, this can be done by organizing the buttons
    # with in an inner object holder but creating them as objects of the outer frame. When the buttons are pressed, the
    # listbox list will change appropriately, and the buttons will stay pressed.
    # The list of items in the listbox will be double clickable and will open a
    # pop out window that will actually display the item.
    # There will only be one window open at any given time.
    # Any attempts to open a new item will simply change the item displayed in the current window.

    def grid_items(self):
        pass

    def save(self):
        pass


class MiscButtonHolder(CustomHolderFrame):
    def save(self):
        pass

    def grid_items(self):
        pass