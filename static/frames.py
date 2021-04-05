import tkinter as tk
from abc import ABC, abstractmethod
from character import character
from static.settings import *
from static.widgets import *


# abstract class for the cards that hold all other cards, used to define style and look
class LevelOneCard(ABC, tk.LabelFrame):
    def __init__(self, parent, title, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)

        self.frame_label = tk.Label(self, text=title, font=(None, 20))

        self.widgets = []
        self.entries = []

    @abstractmethod
    def grid_items(self):
        pass

    # used to call the grid item function for all inner widgets
    def inner_grid(self):
        for widget in self.widgets:
            widget.grid_items()

    # calls save function for all inner widgets
    def save(self):
        for widget in self.widgets:
            widget.save()


# Displays all basic and Misc info as inner cards
class BasicInfoCard(LevelOneCard):
    def __init__(self, parent, title, *args, **kwargs):
        LevelOneCard.__init__(self, parent, title, *args, **kwargs)
        self.misc_card = MiscCard(self, 'Miscellaneous')
        self.abilities_card = AbilityCard(self, 'Ability Scores')
        self.saves_card = SavesCard(self, 'Saving Throws')
        self.skill_card = SkillsCard(self, 'Skills')
        self.gold_card = GoldCard(self, 'Gold')

        self.misc_features_card = MiscItemsMenuCard(self, 'Features')

        self.widgets.append(self.misc_card)
        self.widgets.append(self.abilities_card)
        self.widgets.append(self.saves_card)
        self.widgets.append(self.skill_card)
        self.widgets.append(self.gold_card)
        self.widgets.append(self.misc_features_card)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)
        self.misc_card.grid(row=1, column=0)
        self.abilities_card.grid(row=1, column=1)
        self.saves_card.grid(row=1, column=2)
        self.skill_card.grid(row=1, column=3)
        self.gold_card.grid(row=1, column=4)
        self.misc_features_card.grid(row=2, column=1)


# displays most info relating to combat as inner frame
class BasicCombatCard(LevelOneCard):
    def __init__(self, parent, title, *args, **kwargs):
        LevelOneCard.__init__(self, parent, title, *args, **kwargs)

        self.top_card = TopCombatCard(self, 'Top Stats')
        self.hp_card = HitPointsCard(self, 'Hit Points')
        self.hdice_card = HitDiceCard(self, 'Hit Dice')
        self.death_card = DeathSavesCard(self, 'Death Saves')
        # self.attacks_card = WeaponItemsMenu(self, 'Attacks')
        self.attacks_card = MiscButton(self, text='Attacks', command=self.open_item)

        self.widgets.append(self.top_card)
        self.widgets.append(self.hp_card)
        self.widgets.append(self.hdice_card)
        self.widgets.append(self.death_card)
        self.widgets.append(self.attacks_card)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        self.top_card.grid(row=1, column=0, columnspan=3)
        self.hp_card.grid(row=2, column=0)
        self.hdice_card.grid(row=2, column=1)
        self.death_card.grid(row=2, column=2)
        self.attacks_card.grid(row=3, column=0, columnspan=3)

    def open_item(self):
        if not character.open_item:
            menu = WeaponItemWindow2(self, title='Attacks Menu')

            character.open_item = True


class BasicSpellcastingCard(LevelOneCard):
    def __init__(self, parent, title, *args, **kwargs):
        LevelOneCard.__init__(self, parent, title, *args, **kwargs)

        self.basics_card = SpellBasics(self, 'Spell Basics')

        self.widgets.append(self.basics_card)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        self.basics_card.grid(row=1, column=0)


# Card (frame) where all information is displayed.
# inner widgets hold most logic relating to backend
class LevelTwoCard(tk.LabelFrame, FrameTemplate, ABC):
    DICT = {}

    def __init__(self, parent, title, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        FrameTemplate.__init__(self, *args, **kwargs)

        self.frame_label = tk.Label(self, text=title, font=(None, 17))
        self.parent = parent


# this card displays all info relating to the character at a surface level
# mainly used for information that describes the character in broad strokes
class MiscCard(LevelTwoCard):
    DICT = {'Name': 'name',
            'Class & Level': 'class_level',
            'Background': 'background',
            'Race': 'race',
            'Alignment': 'alignment',
            'Proficiency': 'proficiency'}

    def create_widgets(self, key, values):
        if values == 'proficiency':
            return LabelEntryPair(self, entry_type=NumberEntry, label_text=key, attr=values)
        else:
            return LabelEntryPair(self, entry_type=TextEntry, label_text=key, attr=values)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        self.widgets[0].grid(row=1, column=0, sticky=tk.E)
        self.widgets[1].grid(row=2, column=0, sticky=tk.E)
        self.widgets[2].grid(row=3, column=0, sticky=tk.E)
        self.widgets[3].grid(row=4, column=0, sticky=tk.E)
        self.widgets[4].grid(row=5, column=0, sticky=tk.E)
        self.widgets[5].grid(row=6, column=0, sticky=tk.E)


# displays character's ability scores. each label and entry are generated using the LabelEntryPair widget
class AbilityCard(LevelTwoCard):
    DICT = {'Strength': 'strength',
            'Dexterity': 'dexterity',
            'Constitution': 'constitution',
            'Intelligence': 'intelligence',
            'Wisdom': 'wisdom',
            'Charisma': 'charisma'}

    def create_widgets(self, key, values):
        pair = LabelEntryPair(self, entry_type=NumberEntry, label_text=key, attr=values)
        pair.add_mod()
        return pair

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        self.widgets[0].grid(row=1, column=0, sticky=tk.E)
        self.widgets[1].grid(row=2, column=0, sticky=tk.E)
        self.widgets[2].grid(row=3, column=0, sticky=tk.E)
        self.widgets[3].grid(row=4, column=0, sticky=tk.E)
        self.widgets[4].grid(row=5, column=0, sticky=tk.E)
        self.widgets[5].grid(row=6, column=0, sticky=tk.E)


# Displays the characters Saving throws
# uses checkbuttons and labels to display proficiency and modifiers
class SavesCard(LevelTwoCard):
    DICT = {'Strength': ['strength_throw', 'strength'],
            'Dexterity': ['dexterity_throw', 'dexterity'],
            'Constitution': ['constitution_throw', 'dexterity'],
            'Intelligence': ['intelligence_throw', 'intelligence'],
            'Wisdom': ['wisdom_throw', 'wisdom'],
            'Charisma': ['charisma_throw', 'charisma']}

    def create_widgets(self, key, values):
        return CheckLabelPair(self, attr1=values[1], attr2=values[0], label_text=key)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        self.widgets[0].grid(row=1, column=0, sticky=tk.E)
        self.widgets[1].grid(row=2, column=0, sticky=tk.E)
        self.widgets[2].grid(row=3, column=0, sticky=tk.E)
        self.widgets[3].grid(row=4, column=0, sticky=tk.E)
        self.widgets[4].grid(row=5, column=0, sticky=tk.E)
        self.widgets[5].grid(row=6, column=0, sticky=tk.E)


# displays the characters skills in much the same way as saving throws
# each skill is called in the dict using its proficiency and its associated ability score
class SkillsCard(LevelTwoCard):
    DICT = {'Acrobatics': ['acrobatics', 'dexterity'],
            'Animal Handling': ['animal', 'wisdom'],
            'Arcana': ['arcana', 'intelligence'],
            'Athletics': ['athletics', 'strength'],
            'Deception': ['deception', 'charisma'],
            'History': ['history', 'intelligence'],
            'Insight': ['insight', 'wisdom'],
            'Intimidation': ['intimidation', 'charisma'],
            'Investigation': ['investigation', 'intelligence'],
            'Medicine': ['medicine', 'wisdom'],
            'Nature': ['nature', 'intelligence'],
            'Perception': ['perception', 'wisdom'],
            'Performance': ['performance', 'charisma'],
            'Persuasion': ['persuasion', 'charisma'],
            'Religion': ['religion', 'intelligence'],
            'Sleight of Hand': ['sleight', 'dexterity'],
            'Stealth': ['stealth', 'dexterity'],
            'Survival': ['survival', 'wisdom']}

    # this function is deprecated and should be removed after testing
    def pair_factory(self):
        for key, values in self.DICT.items():
            self.widgets.append(self.create_widgets(key, values))

    def create_widgets(self, key, values):
        return CheckLabelPair(self, attr1=values[1], attr2=values[0], label_text=key)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        self.widgets[0].grid(row=1, column=0, sticky=tk.E)
        self.widgets[1].grid(row=2, column=0, sticky=tk.E)
        self.widgets[2].grid(row=3, column=0, sticky=tk.E)
        self.widgets[3].grid(row=4, column=0, sticky=tk.E)
        self.widgets[4].grid(row=5, column=0, sticky=tk.E)
        self.widgets[5].grid(row=6, column=0, sticky=tk.E)
        self.widgets[6].grid(row=7, column=0, sticky=tk.E)
        self.widgets[7].grid(row=8, column=0, sticky=tk.E)
        self.widgets[8].grid(row=9, column=0, sticky=tk.E)
        self.widgets[9].grid(row=10, column=0, sticky=tk.E)
        self.widgets[10].grid(row=11, column=0, sticky=tk.E)
        self.widgets[11].grid(row=12, column=0, sticky=tk.E)
        self.widgets[12].grid(row=13, column=0, sticky=tk.E)
        self.widgets[13].grid(row=14, column=0, sticky=tk.E)
        self.widgets[14].grid(row=15, column=0, sticky=tk.E)
        self.widgets[15].grid(row=16, column=0, sticky=tk.E)
        self.widgets[16].grid(row=17, column=0, sticky=tk.E)
        self.widgets[17].grid(row=18, column=0, sticky=tk.E)


# Displays characters current gold
class GoldCard(LevelTwoCard):
    DICT = {'Copper': 'cp',
            'Silver': 'sp',
            'Electrum': 'ep',
            'Gold': 'gp',
            'Platinum': 'pp'}

    def create_widgets(self, key, values):
        return LabelEntryPair(self, entry_type=NumberEntry, label_text=key, attr=values)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        self.widgets[0].grid(row=1, column=0, sticky=tk.E)
        self.widgets[1].grid(row=2, column=0, sticky=tk.E)
        self.widgets[2].grid(row=3, column=0, sticky=tk.E)
        self.widgets[3].grid(row=4, column=0, sticky=tk.E)
        self.widgets[4].grid(row=5, column=0, sticky=tk.E)


class HitPointsCard(LevelTwoCard):
    DICT = {'Maximum': 'hp_maximum',
            'Current': 'current_hp',
            'Temporary': 'temporary_hp'}

    def create_widgets(self, key, values):
        return LabelEntryPair(self, entry_type=NumberEntry, label_text=key, attr=values)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        self.widgets[0].grid(row=1, column=0, sticky=tk.E)
        self.widgets[1].grid(row=2, column=0, sticky=tk.E)
        self.widgets[2].grid(row=3, column=0, sticky=tk.E)


class HitDiceCard(LevelTwoCard):
    DICT = {'Total': 'total_dice',
            'Current': 'current_dice'}

    def create_widgets(self, key, values):
        return LabelEntryPair(self, entry_type=NumberEntry, label_text=key, attr=values)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        self.widgets[0].grid(row=1, column=0, sticky=tk.E)
        self.widgets[1].grid(row=2, column=0, sticky=tk.E)


class DeathSavesCard(LevelTwoCard):
    DICT = {'Successes': 'success_throws',
            'Failures': 'fail_throws'}

    def create_widgets(self, key, values):
        return LabelEntryPair(self, entry_type=NumberEntry, label_text=key, attr=values)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        self.widgets[0].grid(row=1, column=0, sticky=tk.E)
        self.widgets[1].grid(row=2, column=0, sticky=tk.E)


class TopCombatCard(LevelTwoCard):
    DICT = {'Armor Class': 'armor_class',
            'Initiative': 'initiative',
            'Speed': 'speed'}

    def create_widgets(self, key, values):
        return LabelEntryPair(self, label_text=key, attr=values, entry_type=NumberEntry, style='top combat')

    def grid_items(self):
        self.inner_grid()

        self.widgets[0].grid(row=1, column=0, sticky=tk.E)
        self.widgets[1].grid(row=1, column=1, sticky=tk.E)
        self.widgets[2].grid(row=1, column=2, sticky=tk.E)


class SelectMenu(LevelTwoCard, ABC):

    def change_list(self, list_type, btn):
        self.entries[0] = list_type
        self.change_btn(btn)
        self.widgets[1].change_list(list_type)

    def change_btn(self, btn):
        if self.entries[1]:
            self.entries[1].release()
        self.entries[1] = self.widgets[btn]
        self.entries[1].pressed()

    @abstractmethod
    def open_item(self, *args):
        pass

    @abstractmethod
    def add_item(self):
        pass

    def refresh(self):
        self.widgets[1].change_list(self.entries[0])


class MiscItemsMenuCard(SelectMenu):
    DICT = {'Button Holder': 'button_holder',
            'List_Box': 'list_box',
            'Personality Traits': ['personality', 2],
            'Ideals': ['ideals', 3],
            'Bonds': ['bonds', 4],
            'Flaws': ['flaws', 5],
            'Features': ['features', 6],
            'Equipment': ['equipment', 7],
            'Proficiencies': ['other_prof', 8],
            'Languages': ['languages', 9],
            'Add': 'add',
            }

    def create_widgets(self, key, values):
        if values == 'list_box':
            listbox = MiscListbox(self)
            listbox.bind("<<ListboxSelect>>", lambda event: self.open_item(listbox.get_selection()))
            return listbox
        elif values == 'button_holder':
            return ButtonHolder(self)
        elif values == 'add':
            return MiscButton(self.widgets[0], text=key, command=self.add_item)
        else:
            return MiscButton(self.widgets[0], text=key, command=lambda: self.change_list(values[0], values[1]))

    def grid_items(self):
        self.inner_grid()

        self.entries.append(None)
        self.entries.append(None)
        self.change_list('personality', 2)

        self.widgets[0].grid(row=0, column=0)
        self.widgets[1].grid(row=0, column=1)
        self.widgets[2].grid(row=0, column=0, sticky=tk.N+tk.EW)
        self.widgets[3].grid(row=1, column=0, sticky=tk.N+tk.EW)
        self.widgets[4].grid(row=2, column=0, sticky=tk.N+tk.EW)
        self.widgets[5].grid(row=3, column=0, sticky=tk.N+tk.EW)
        self.widgets[6].grid(row=4, column=0, sticky=tk.N+tk.EW)
        self.widgets[7].grid(row=5, column=0, sticky=tk.N+tk.EW)
        self.widgets[8].grid(row=6, column=0, sticky=tk.N+tk.EW)
        self.widgets[9].grid(row=7, column=0, sticky=tk.N+tk.EW)
        self.widgets[10].grid(row=8, column=0, sticky=tk.N+tk.EW)

    def open_item(self, selection):
        if not character.open_item:
            MiscItemWindow(self, selection)
            character.open_item = True

    def add_item(self):
        if not character.open_item:
            MiscItemWindow(self, 'New Item', self.entries[0])
            character.open_item = True


class WeaponItemsMenu(SelectMenu):
    DICT = {'Button Holder': 'button_holder',
            'List_Box': 'list_box',
            'Weapons': ['weapon', 2],
            'Physical Attacks': ['non_weapon', 3],
            'Add': 'add'
            }

    def create_widgets(self, key, values):
        if values == 'list_box':
            listbox = WeaponsListbox(self)
            listbox.bind("<<ListboxSelect>>", lambda event: self.open_item(listbox.get_selection()))
            return listbox
        elif values == 'button_holder':
            return ButtonHolder(self)
        elif values == 'add':
            return MiscButton(self.widgets[0], text=key, command=self.add_item)
        else:
            return MiscButton(self.widgets[0], text=key, command=lambda: self.change_list(values[0], values[1]))

    def grid_items(self):
        self.inner_grid()

        self.entries.append(None)
        self.entries.append(None)
        self.change_list('weapon', 2)

        self.widgets[0].grid(row=0, column=0)
        self.widgets[1].grid(row=0, column=1)
        self.widgets[2].grid(row=0, column=0, sticky=tk.N + tk.EW)
        self.widgets[3].grid(row=1, column=0, sticky=tk.N + tk.EW)
        self.widgets[4].grid(row=2, column=0, sticky=tk.N + tk.EW)

    def open_item(self, selection):
        self.parent.open_item(selection)

    def add_item(self):
        self.parent.add_item()


class SpellBasics(LevelTwoCard):
    DICT = {'Casting Ablility': 'casting_ability',
            'Spell Save DC': 'spell_save_dc',
            'Spell Attack Bonus': 'spell_atk_bonus',
            'Spell Book': 'spell_book'}

    def create_widgets(self, key, values):
        if values == 'spell_book':
            return SpellBookButton(self, text=key, command=self.open_spell_book)
        return LabelEntryPair(self, label_text=key, attr=values, entry_type=TextEntry, style='spell basics')

    def grid_items(self):
        self.inner_grid()

        self.widgets[0].grid(row=0, column=0)
        self.widgets[1].grid(row=1, column=0)
        self.widgets[2].grid(row=2, column=0)
        self.widgets[3].grid(row=3, column=0)

    def open_spell_book(self):
        if not character.open_spell_book:
            self.widgets[3].pressed()
            character.open_item = True


class PopupWindow(FrameTemplate, tk.Toplevel, ABC):
    def __init__(self, parent, title, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        FrameTemplate.__init__(self, *args, **kwargs)
        self.title(title)
        self.parent = parent

    def on_exit(self):
        character.open_item = False
        self.parent.refresh()
        self.destroy()

    def grid_items(self):
        self.inner_grid()
        self.widgets[0].grid(row=0, column=0)


class MiscItemWindow(PopupWindow):
    DICT = {'Display': 'display'}

    def __init__(self, parent, title, list_type=None, *args, **kwargs):
        self.title_string = title
        if title == 'New Item':
            self.item = list_type
        else:
            self.item = character.misc_items.get_item(title)
        PopupWindow.__init__(self, parent, title, *args, **kwargs)

        self.grid_items()

    def create_widgets(self, key, values):
        if self.title_string == 'New Item':
            return MiscAddDisplay(self, self.item)
        else:
            return MiscItemDisplay(self, self.item)


class WeaponItemWindow(PopupWindow):
    DICT = {'Display': 'display'}

    def __init__(self, parent, title, list_type=None, *args, **kwargs):
        self.title_string = title
        if title == 'New Item':
            self.item = list_type
        else:
            self.item = character.weapon_items.get_item(title)
        PopupWindow.__init__(self, parent, title, *args, **kwargs)

        self.grid_items()

    def create_widgets(self, key, values):
        if self.title_string == 'New Item':
            return WeaponAddDisplay(self, self.item)
        else:
            return WeaponItemDisplay(self, self.item)


class WeaponItemWindow2(PopupWindow):
    DICT = {'Selection': 'select',
            'Display': 'display'}

    def __init__(self, parent, title, list_type=None, *args, **kwargs):
        PopupWindow.__init__(self, parent, title, *args, **kwargs)

        self.list_type = None
        self.grid_items()

    def create_widgets(self, key, values):
        if values == 'select':
            return WeaponItemsMenu(self, 'Attacks')
        elif values == 'display':
            return WeaponItemDisplay(self)

    def grid_items(self):
        self.inner_grid()
        self.widgets[0].grid(row=0, column=0)
        self.widgets[1].grid(row=0, column=1)

    def open_item(self, selection):
        self.widgets[1].item_mode(character.weapon_items.get_item(selection))

    def add_item(self):
        self.widgets[1].add_mode()

    def on_exit(self):
        character.open_item = False
        self.destroy()