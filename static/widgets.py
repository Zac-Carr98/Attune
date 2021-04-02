import tkinter as tk
from abc import ABC, abstractmethod
from character import character
from static.settings import *
import static_functions as sf


class FrameTemplate(ABC):
    DICT = {}

    def __init__(self, *args, **kwargs):

        self.widgets = []
        self.entries = []

        self.widget_factory()

    @abstractmethod
    def grid_items(self):
        pass

    # this runs through any given cards dicts and creates the
    # widgets as defined on the card in "create_widgets" function
    def widget_factory(self):
        for key, values in self.DICT.items():
            self.widgets.append(self.create_widgets(key, values))

    @abstractmethod
    def create_widgets(self, key, values):
        pass

    def inner_grid(self):
        for widget in self.widgets:
            widget.grid_items()

    def save(self):
        for widget in self.widgets:
            widget.save()


class CustomHolderFrame(ABC, tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.item = None
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

    def grid_items(self):
        pass

    def save(self):
        pass


class MiscButton(CustomButton):
    def __init__(self, parent, *args, **kwargs):
        CustomButton.__init__(self, parent, *args, **kwargs)

    def pressed(self):
        self.config(relief=tk.SUNKEN)

    def release(self):
        self.config(relief=tk.RAISED)


class CustomListbox(ABC, tk.Listbox):
    def __init__(self, parent, *args, **kwargs):
        tk.Listbox.__init__(self, parent, *args, **kwargs)

    def set_list(self, item_list):
        for item in reversed(item_list):
            self.insert(0, item['name'])

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

    def change_list(self, list_type):
        self.clear()
        self.set_list(item_list=character.misc_type_list(list_type))


class WeaponsListbox(CustomListbox):
    def __init__(self, parent, *args, **kwargs):
        CustomListbox.__init__(self, parent, *args, **kwargs)
        self.config(width=20, height=12, font=(None, 14))

    def change_list(self, list_type):
        self.clear()
        self.set_list(item_list=character.weapon_type_list(list_type))

    def set_list(self, item_list):
        for item in reversed(item_list):
            self.insert(0, f"{item['name']}")


class ButtonHolder(CustomHolderFrame):
    def save(self):
        pass

    def grid_items(self):
        pass


class MiscItemDisplay(FrameTemplate, tk.Frame):
    DICT = {'Name': 'name',
            'Description': 'desc',
            'Save Changes': 'save_btn',
            'Delete': 'delete'}

    def __init__(self, parent, item, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        FrameTemplate.__init__(self, *args, **kwargs)
        self.item = item
        self.parent = parent

        self.set_widgets()

    def create_widgets(self, key, values):
        if values == 'name':
            return MiscItemPair(self, attr=None, entry_type=TextEntry, label_text=key)
        elif values == 'desc':
            return MiscItemPair(self, attr=None, entry_type=CustomTextbox, label_text=key, style='textbox')
        elif values == 'save_btn':
            return MiscButton(self, text=key, command=self.save)
        elif values == 'delete':
            return MiscButton(self, text=key, command=self.delete)

    def set_widgets(self):
        self.widgets[0].set_entry(self.item['name'])
        self.widgets[1].set_entry(self.item['description'])

    def grid_items(self):
        self.inner_grid()

        self.widgets[0].grid(row=0, column=0, sticky=tk.W)
        self.widgets[1].grid(row=1, column=0, columnspan=3)
        self.widgets[2].grid(row=0, column=1)
        self.widgets[3].grid(row=0, column=2)

    def save(self):
        self.item['name'] = self.widgets[0].get_entry()
        self.item['description'] = self.widgets[1].get_entry()
        character.misc_items.update(self.item)

    def delete(self):
        character.misc_items.delete(self.item['id'])
        self.parent.on_exit()


class MiscAddDisplay(FrameTemplate, tk.Frame):
    DICT = {'Name': 'name',
            'Description': 'desc',
            'Save & Close': 'save_btn'}

    def __init__(self, parent, list_type, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        FrameTemplate.__init__(self, *args, **kwargs)
        self.parent = parent
        self.list_type = list_type

    def create_widgets(self, key, values):
        if values == 'name':
            return MiscItemPair(self, attr=None, entry_type=TextEntry, label_text=key)
        elif values == 'desc':
            return MiscItemPair(self, attr=None, entry_type=CustomTextbox, label_text=key, style='textbox')
        elif values == 'save_btn':
            return MiscButton(self, text=key, command=self.save)

    def grid_items(self):
        self.inner_grid()

        self.widgets[0].grid(row=0, column=0, sticky=tk.W)
        self.widgets[1].grid(row=1, column=0, columnspan=2)
        self.widgets[2].grid(row=0, column=1)

    def save(self):
        character.misc_items.add_item(name=self.widgets[0].get_entry(),
                                      description=self.widgets[1].get_entry(),
                                      list_type=self.list_type)
        self.parent.on_exit()


class WeaponItemDisplay(FrameTemplate, tk.Frame):
    DICT = {'Name': 'name',
            'Attack Bonus': 'atk_bns',
            'Damage': 'damage',
            'Description': 'desc',
            'Save Changes': 'save_btn',
            'Delete': 'delete'}

    def __init__(self, parent, item, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        FrameTemplate.__init__(self, *args, **kwargs)
        self.item = item
        self.parent = parent

        self.set_widgets()

    def create_widgets(self, key, values):
        if values == 'name':
            return MiscItemPair(self, attr=None, entry_type=TextEntry, label_text=key)
        elif values == 'atk_bns':
            return MiscItemPair(self, attr=None, entry_type=TextEntry, label_text=key)
        elif values == 'damage':
            return MiscItemPair(self, attr=None, entry_type=TextEntry, label_text=key)
        elif values == 'desc':
            return MiscItemPair(self, attr=None, entry_type=CustomTextbox, label_text=key, style='textbox')
        elif values == 'save_btn':
            return MiscButton(self, text=key, command=self.save)
        elif values == 'delete':
            return MiscButton(self, text=key, command=self.delete)

    def set_widgets(self):
        self.widgets[0].set_entry(self.item['name'])
        self.widgets[1].set_entry(self.item['atk_bns'])
        self.widgets[2].set_entry(self.item['damage'])
        self.widgets[3].set_entry(self.item['description'])

    def grid_items(self):
        self.inner_grid()

        self.widgets[0].grid(row=0, column=0, sticky=tk.W)
        self.widgets[1].grid(row=1, column=0, sticky=tk.W)
        self.widgets[2].grid(row=2, column=0, sticky=tk.W)
        self.widgets[3].grid(row=3, column=0, columnspan=3)
        self.widgets[4].grid(row=0, column=1)
        self.widgets[5].grid(row=0, column=2)

    def save(self):
        self.item['name'] = self.widgets[0].get_entry()
        self.item['atk_bns'] = self.widgets[1].get_entry()
        self.item['damage'] = self.widgets[2].get_entry()
        self.item['description'] = self.widgets[3].get_entry()
        character.weapon_items.update(self.item)

    def delete(self):
        character.weapon_items.delete(self.item['id'])
        self.parent.on_exit()


class WeaponAddDisplay(FrameTemplate, tk.Frame):
    DICT = {'Name': 'name',
            'Attack Bonus': 'atk_bns',
            'Damage': 'damage',
            'Description': 'desc',
            'Save & Close': 'save_btn'}

    def __init__(self, parent, list_type, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        FrameTemplate.__init__(self, *args, **kwargs)
        self.parent = parent
        self.list_type = list_type

    def create_widgets(self, key, values):
        if values == 'name':
            return MiscItemPair(self, attr=None, entry_type=TextEntry, label_text=key)
        elif values == 'atk_bns':
            return MiscItemPair(self, attr=None, entry_type=TextEntry, label_text=key)
        elif values == 'damage':
            return MiscItemPair(self, attr=None, entry_type=TextEntry, label_text=key)
        elif values == 'desc':
            return MiscItemPair(self, attr=None, entry_type=CustomTextbox, label_text=key, style='textbox')
        elif values == 'save_btn':
            return MiscButton(self, text=key, command=self.save)

    def grid_items(self):
        self.inner_grid()

        self.widgets[0].grid(row=0, column=0, sticky=tk.W)
        self.widgets[1].grid(row=1, column=0, sticky=tk.W)
        self.widgets[2].grid(row=2, column=0, sticky=tk.W)
        self.widgets[3].grid(row=3, column=0, columnspan=2)
        self.widgets[4].grid(row=0, column=1, sticky=tk.W)

    def save(self):
        character.weapon_items.add_item(name=self.widgets[0].get_entry(),
                                        atk_bns=self.widgets[1].get_entry(),
                                        damage=self.widgets[2].get_entry(),
                                        description=self.widgets[3].get_entry(),
                                        list_type=self.list_type)
        self.parent.on_exit()
