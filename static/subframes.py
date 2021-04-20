import tkinter as tk
from abc import ABC, abstractmethod
from character import character
from static.settings import *
from static.widgets import *


class ItemDisplay(FrameTemplate, tk.Frame, ABC):
    DICT = {}

    def __init__(self, parent, item=None, list_type=None, *args, **kwargs):
        self.item = item
        tk.Frame.__init__(self, parent, *args, **kwargs)
        FrameTemplate.__init__(self, *args, **kwargs)
        self.config(bg=LEVELTWO)

        self.parent = parent
        self.list_type = list_type

        if self.item:
            self.set_widgets()

    @abstractmethod
    def set_widgets(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    def create_widgets(self, key, values):
        if values in ('name', 'atk_bns', 'damage', 'casting_time', 'range', 'components', 'duration', 'school'):
            label = LevelTwoLabel(self, text=key)
            entry = ItemTextEntry(self)
            if self.item:
                entry.set_entry(self.item[values])
            return [label, entry]
        elif values == 'description':
            entry = CustomTextbox(self)
            if self.item:
                entry.set_entry(self.item[values])
            return entry
        elif values == 'save_btn':
            return MiscButton(self, text=key, command=self.save)
        elif values == 'delete':
            return MiscButton(self, text=key, command=self.delete)


class MiscItemDisplay(ItemDisplay):
    DICT = {'Name': 'name',
            'Description': 'description',
            'Save Changes': 'save_btn',
            'Delete': 'delete'}

    def set_widgets(self):
        # self.widgets[0].set_entry(self.item['name'])
        # self.widgets[1].set_entry(self.item['description'])
        pass

    def grid_items(self):
        self.inner_grid()

        self.widgets[0][0].grid(row=0, column=0, sticky=tk.W)
        self.widgets[0][1].grid(row=0, column=1, sticky=tk.W)
        self.widgets[1].grid(row=1, column=0, columnspan=3)
        self.widgets[2].grid(row=0, column=2)
        self.widgets[3].grid(row=0, column=3)

    def save(self):
        if self.item:
            self.item['name'] = self.widgets[0][1].get_entry()
            self.item['description'] = self.widgets[1].get_entry()
            character.misc_items.update(self.item)
        else:
            character.misc_items.add_item(name=self.widgets[0][1].get_entry(),
                                          description=self.widgets[1].get_entry(),
                                          list_type=self.list_type)
            self.parent.on_exit()

    def delete(self):
        character.misc_items.delete(self.item['id'])
        self.parent.on_exit()

    def add_mode(self):
        self.item = None
        for i in range(0, 2):
            self.widgets[i].reset()
        self.widgets[3].grid_forget()

    def item_mode(self, item):
        self.item = item
        self.set_widgets()
        self.widgets[3].grid(row=0, column=2)


class WeaponItemDisplay(ItemDisplay):
    DICT = {'Name': 'name',
            'Attack Bonus': 'atk_bns',
            'Damage': 'damage',
            'Description': 'description',
            'Save Changes': 'save_btn',
            'Delete': 'delete'}

    def set_widgets(self):
        self.widgets[0][1].set_entry(self.item['name'])
        self.widgets[1][1].set_entry(self.item['atk_bns'])
        self.widgets[2][1].set_entry(self.item['damage'])
        self.widgets[3].set_entry(self.item['description'])
        pass

    def grid_items(self):
        self.inner_grid()

        self.widgets[0][0].grid(row=0, column=0, sticky=tk.W)
        self.widgets[0][1].grid(row=0, column=1, sticky=tk.W)
        self.widgets[1][0].grid(row=1, column=0, sticky=tk.W)
        self.widgets[1][1].grid(row=1, column=1, sticky=tk.W)
        self.widgets[2][0].grid(row=2, column=0, sticky=tk.W)
        self.widgets[2][1].grid(row=2, column=1, sticky=tk.W)
        self.widgets[3].grid(row=3, column=0, columnspan=3)
        self.widgets[4].grid(row=0, column=2)

    def save(self):
        if self.item:
            self.item['name'] = self.widgets[0][1].get_entry()
            self.item['atk_bns'] = self.widgets[1][1].get_entry()
            self.item['damage'] = self.widgets[2][1].get_entry()
            self.item['description'] = self.widgets[3].get_entry()
            character.weapon_items.update(self.item)

        else:
            character.weapon_items.add_item(name=self.widgets[0][1].get_entry(),
                                            atk_bns=self.widgets[1][1].get_entry(),
                                            damage=self.widgets[2][1].get_entry(),
                                            description=self.widgets[3].get_entry(),
                                            list_type=self.parent.widgets[0].entries[0])
        self.parent.widgets[0].refresh()

    def delete(self):
        character.weapon_items.delete(self.item['id'])
        self.parent.widgets[0].refresh()
        self.add_mode()

    def add_mode(self):
        self.item = None
        for i in range(0, 4):
            if i == 3:
                self.widgets[i].reset()
            else:
                self.widgets[i][1].reset()
        self.widgets[5].grid_forget()

    def item_mode(self, item):
        self.item = item
        self.set_widgets()
        self.widgets[5].grid(row=1, column=2)


class SpellItemDisplay(ItemDisplay):
    DICT = {'Name': 'name',
            'Casting Time': 'casting_time',
            'Range': 'range',
            'Components': 'components',
            'Duration': 'duration',
            'School': 'school',
            'Description': 'description',
            'Save Changes': 'save_btn',
            'Delete': 'delete'}

    def set_widgets(self):
        self.widgets[0][1].set_entry(self.item['name'])
        self.widgets[1][1].set_entry(self.item['casting_time'])
        self.widgets[2][1].set_entry(self.item['range'])
        self.widgets[3][1].set_entry(self.item['components'])
        self.widgets[4][1].set_entry(self.item['duration'])
        self.widgets[5][1].set_entry(self.item['school'])
        self.widgets[6].set_entry(self.item['description'])

    def grid_items(self):
        self.inner_grid()

        self.widgets[0][0].grid(row=0, column=0, sticky=tk.W)
        self.widgets[0][1].grid(row=0, column=1, sticky=tk.W)
        self.widgets[1][0].grid(row=1, column=0, sticky=tk.W)
        self.widgets[1][1].grid(row=1, column=1, sticky=tk.W)
        self.widgets[2][0].grid(row=2, column=0, sticky=tk.W)
        self.widgets[2][1].grid(row=2, column=1, sticky=tk.W)
        self.widgets[3][0].grid(row=0, column=2, sticky=tk.W)
        self.widgets[3][1].grid(row=0, column=3, sticky=tk.W)
        self.widgets[4][0].grid(row=1, column=2, sticky=tk.W)
        self.widgets[4][1].grid(row=1, column=3, sticky=tk.W)
        self.widgets[5][0].grid(row=2, column=2, sticky=tk.W)
        self.widgets[5][1].grid(row=2, column=3, sticky=tk.W)
        self.widgets[6].grid(row=3, column=0, columnspan=5, sticky=tk.W)
        self.widgets[7].grid(row=0, column=4)

    def delete(self):
        character.spell_items.delete(self.item['id'])
        self.parent.widgets[0].refresh()
        self.add_mode()

    def add_mode(self):
        self.item = None
        for i in range(0, 7):
            if i == 6:
                self.widgets[i].reset()
            else:
                self.widgets[i][1].reset()
        self.widgets[8].grid_forget()

    def item_mode(self, item):
        self.item = item
        self.set_widgets()
        self.widgets[8].grid(row=1, column=4)

    def save(self):
        if self.item:
            for index, value in enumerate(self.DICT.values()):
                if index in range(0, 6):
                    self.item[value] = self.widgets[index][1].get_entry()
                elif index == 6:
                    self.item[value] = self.widgets[index].get_entry()

            character.spell_items.update(self.item)

        else:
            character.spell_items.add_item(name=self.widgets[0][1].get_entry(),
                                           casting_time=self.widgets[1][1].get_entry(),
                                           spell_range=self.widgets[2][1].get_entry(),
                                           components=self.widgets[3][1].get_entry(),
                                           duration=self.widgets[4][1].get_entry(),
                                           school=self.widgets[5][1].get_entry(),
                                           description=self.widgets[6].get_entry(),
                                           level=self.parent.widgets[0].entries[0])
        self.parent.widgets[0].refresh()
