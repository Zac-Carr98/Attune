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
            if isinstance(widget, list):
                for j in widget:
                    j.grid_items()
            else:
                widget.grid_items()

    def save(self):
        for widget in self.widgets:
            if isinstance(widget, list):
                for j in widget:
                    j.save()
            else:
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


class SpellSlotDisplay(FrameTemplate, tk.Frame):
    DICT = {'Max': 'max',
            'Used': 'used'}

    def __init__(self, parent, max_ss, current_ss, *args, **kwargs):
        self.max_ss = max_ss
        self.current_ss = current_ss
        tk.Frame.__init__(self, parent, *args, **kwargs)
        FrameTemplate.__init__(self, parent, *args, **kwargs)

    def create_widgets(self, key, values):
        if values == 'max':
            return NumberEntry(self, self.max_ss)
        elif values == 'used':
            return NumberEntry(self, self.current_ss)

    def grid_items(self):
        self.widgets[0].grid(row=0, column=0)
        self.widgets[1].grid(row=0, column=1)


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
        self.config(bg=LEVELTWO)

        self.entry_type = entry_type
        self.entry = entry_type(self)
        self.label = LevelTwoLabel(self, text=label_text)
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

        if self.style == 'spell basics':
            self.label.grid(row=1, column=0)
            self.entry.grid(row=0, column=0)

        elif self.style == 'textbox':
            self.entry.grid(row=0, column=0)

        else:
            self.label.grid(row=0, column=0)
            self.entry.grid(row=0, column=1, sticky=tk.EW)

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


class CustomLabel(ABC, tk.Label):
    def __init__(self, parent, *args, **kwargs):
        tk.Label.__init__(self, parent, *args, **kwargs)

    def grid_items(self):
        pass

    def save(self):
        pass


class LevelOneLabel(CustomLabel):
    def __init__(self, parent, *args, **kwargs):
        CustomLabel.__init__(self, parent, *args, **kwargs)
        self.config(bg=LEVELONE, fg=PRIMARY_TEXT)


class LevelTwoLabel(CustomLabel):
    def __init__(self, parent, *args, **kwargs):
        CustomLabel.__init__(self, parent, *args, **kwargs)
        self.config(bg=LEVELTWO, fg=PRIMARY_TEXT, font=(None, FONT1_SIZE))


class ModLabel(CustomLabel):
    def __init__(self, parent, ability, prof=False, *args, **kwargs):
        CustomLabel.__init__(self, parent, *args, **kwargs)
        self.config(bg=LEVELTWO, fg=PRIMARY_TEXT)

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


class SavingMod(CustomLabel):
    def __init__(self, parent, ability, attr=None, prof=False, *args, **kwargs):
        CustomLabel.__init__(self, parent, *args, **kwargs)
        self.config(bg=LEVELTWO, fg=PRIMARY_TEXT, font=(None, 12))

        self.ability = ability
        self.char_attr = attr
        self.prof = attr

        self.set_label()

    def calculate_mod(self):
        score = character.get_single_attr(self.ability)
        mod = sf.calculate_mod(score)
        return self.check_proficiency(mod)

    def check_proficiency(self, mod):
        if self.prof:
            prof = character.get_single_attr(self.char_attr)
            if prof == 1:
                mod += character.get_single_attr('proficiency')
                return mod
        return mod

    def set_label(self):
        self.config(text=str(self.calculate_mod()))


class AbilitiesMod(SavingMod):
    def __init__(self, parent, ability, attr=None, prof=False, *args, **kwargs):
        SavingMod.__init__(self, parent, ability, *args, **kwargs)
        self.config(font=(None, 18))


class CustomEntry(ABC, tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent, *args, **kwargs)

    @abstractmethod
    def check_entry_type(self):
        pass

    @abstractmethod
    def check_entry_len(self):
        pass

    def grid_items(self):
        pass

    def save(self):
        pass


class NumberEntry(CustomEntry):
    def __init__(self, parent, attr=None, *args, **kwargs):
        CustomEntry.__init__(self, parent, *args, **kwargs)
        self.attr = attr

        self.config(width=4, justify=tk.CENTER)

        if self.attr:
            self.set_entry()

    def check_entry_type(self):
        txt = self.get()
        return txt.isnumeric()

    def check_entry_len(self):
        if len(self.get()) > 4:
            return 'Error, too many digits'

    def set_entry(self):
        self.insert(0, character.get_single_attr(self.attr))

    def save(self):
        character.save_single_attr(self.attr, self.get())


class TextEntry(CustomEntry):
    def __init__(self, parent, attr=None, *args, **kwargs):
        CustomEntry.__init__(self, parent, *args, **kwargs)

        self.config(width=15, justify=tk.CENTER)
        self.attr = attr

        if self.attr:
            self.set_entry()

    def check_entry_type(self):
        return True

    def check_entry_len(self):
        if len(self.get()) > 15:
            return 'Error, too long'

    def get_entry(self):
        return self.get()

    def set_entry(self):
        self.insert(0, character.get_single_attr(self.attr))

    def save(self):
        character.save_single_attr(self.attr, self.get())

    def reset(self):
        self.delete(0, tk.END)


class ItemTextEntry(CustomEntry):
    def __init__(self, parent, attr=None, *args, **kwargs):
        CustomEntry.__init__(self, parent, *args, **kwargs)

        self.config(width=15, justify=tk.CENTER)
        self.attr = attr

        if self.attr:
            self.set_entry()

    def check_entry_type(self):
        return True

    def check_entry_len(self):
        if len(self.get()) > 15:
            return 'Error, too long'

    def get_entry(self):
        return self.get()

    def set_entry(self, entry_text=""):
        self.insert(0, entry_text)

    def save(self):
        pass

    def reset(self):
        self.delete(0, tk.END)


class CustomCheckbutton(tk.Checkbutton):
    def __init__(self, parent, attr, *args, **kwargs):
        self.var = tk.IntVar()
        tk.Checkbutton.__init__(self, parent, variable=self.var, *args, **kwargs)
        self.config(bg=LEVELTWO, activebackground=LEVELTWO,
                    fg=SECONDARY_TEXT, activeforeground=SECONDARY_TEXT,
                    font=(None, FONT1_SIZE))

        self.char_attr = attr

        self.check_proficiency()

    def check_proficiency(self):
        prof = character.get_single_attr(self.char_attr)
        if prof == 1:
            self.var.set(1)

    def grid_items(self):
        pass

    def save(self):
        character.save_single_attr(self.char_attr, self.var.get())


class CustomTextbox(tk.Text):
    def __init__(self, parent, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        self.config(width=50, height=13, wrap=tk.WORD)

    def set_entry(self, entry_text=''):
        self.insert('1.0', entry_text)

    def get_entry(self):
        return self.get('1.0', 'end-1c')

    def reset(self):
        self.delete(1.0, tk.END)

    def grid_items(self):
        pass

    def save(self):
        pass


class CustomButton(ABC, tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.config(font=(None, 12), fg=PRIMARY_TEXT, bg=BUTTON_HIGHLIGHT,
                    activebackground=BUTTON, activeforeground=PRIMARY_TEXT)

    def grid_items(self):
        pass

    def save(self):
        pass


class SpellBookButton(CustomButton):
    def __init__(self, parent, *args, **kwargs):
        CustomButton.__init__(self, parent, *args, **kwargs)

    def pressed(self):
        self.config(relief=tk.SUNKEN)

    def release(self):
        self.config(relief=tk.RAISED)


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
        self.config(width=20, height=20, font=(None, 14))

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


class SpellsListbox(CustomListbox):
    def __init__(self, parent, *args, **kwargs):
        CustomListbox.__init__(self, parent, *args, **kwargs)
        self.config(width=20, height=12, font=(None, 14))

    def change_list(self, list_type):
        self.clear()
        self.set_list(item_list=character.spell_type_list(list_type))

    def set_list(self, item_list):
        for item in reversed(item_list):
            self.insert(0, f"{item['name']}")


class ButtonHolder(CustomHolderFrame):
    def __init__(self, parent, *args, **kwargs):
        CustomHolderFrame.__init__(self, parent, *args, **kwargs)
        self.config(bg=LEVELTWO)
    def save(self):
        pass

    def grid_items(self):
        pass



