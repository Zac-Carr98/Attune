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
        # self.config(bg=LEVELONE)

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

        self.widgets.append(self.top_card)
        self.widgets.append(self.hp_card)
        self.widgets.append(self.hdice_card)
        self.widgets.append(self.death_card)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        self.top_card.grid(row=1, column=0, columnspan=3)
        self.hp_card.grid(row=2, column=0)
        self.hdice_card.grid(row=2, column=1)
        self.death_card.grid(row=2, column=2)


# Card (frame) where all information is displayed.
# inner widgets hold most logic relating to backend
class LevelTwoCard(ABC, tk.LabelFrame):
    DICT = {}

    def __init__(self, parent, title, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)

        self.frame_label = tk.Label(self, text=title, font=(None, 17))

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


# this card is more complicated than the others
# it saves Misc items for the character, listed in the dict,
# the main widget is MiscItem Selection
class MiscFeaturesCard(LevelTwoCard):
    DICT = {'Personality Traits': 'personality',
            'Ideals': 'ideals',
            'Add': 'add',
            'Display': 'display',
            'New Item': 'new_item',
           }

    def create_widgets(self, key, values):
        if values == 'personality':
            return MiscButton(self, text=key, command=lambda: self.change_list(values))
        elif values == 'ideals':
            return MiscButton(self, text=key, command=lambda: self.change_list(values))
        elif values == 'add':
            return MiscButton(self, text=key, command=self.show_add)
        elif values == 'new_item':
            return AddItem(self, label_text='New Item', attr=None)
        elif values == 'display':
            return MiscItemsSelection(self, label_text='Misc Display', attr=None)

    def grid_items(self):
        self.widgets[3].change_list('personality')

        self.inner_grid()

        self.widgets[0].grid(row=0, column=0, sticky=tk.N)
        self.widgets[1].grid(row=1, column=0, sticky=tk.N)
        self.widgets[2].grid(row=2, column=0, sticky=tk.N)
        self.widgets[3].grid(row=0, column=1, rowspan=5)
        # self.widgets[5].grid(row=3, column=0, sticky=tk.N)

    # this function changes the current displayed list of items
    # to match the clicked button
    def change_list(self, list_type, evt=None):
        self.widgets[4].grid_forget()
        self.widgets[3].grid(row=0, column=1, rowspan=5)
        self.widgets[3].change_list(list_type)

    def show_add(self):
        self.widgets[3].grid_forget()
        self.widgets[4].grid(row=0, column=1, rowspan=5)


class MiscItemsMenuCard(LevelTwoCard):
    DICT = {'Button Holder': 'button_holder',
            'List_Box': 'list_box',
            'Personality Traits': 'personality',
            'Ideals': 'ideals',
            'Bonds': 'bonds',
            'Flaws': 'flaws',
            'Features': 'features'
            }

    def create_widgets(self, key, values):
        if values == 'list_box':
            return MiscListbox(self)
        elif values == 'button_holder':
            return MiscButtonHolder(self)
        else:
            return MiscButton(self.widgets[0], text=key, command=lambda: self.change_list(values))

    def grid_items(self):
        self.inner_grid()

        self.widgets[0].grid(row=0, column=0)
        self.widgets[1].grid(row=0, column=1)
        self.widgets[2].grid(row=0, column=0, sticky=tk.N+tk.EW)
        self.widgets[3].grid(row=1, column=0, sticky=tk.N+tk.EW)
        self.widgets[4].grid(row=2, column=0, sticky=tk.N+tk.EW)
        self.widgets[5].grid(row=3, column=0, sticky=tk.N+tk.EW)
        self.widgets[6].grid(row=4, column=0, sticky=tk.N+tk.EW)

    def change_list(self, list_type):
        self.widgets[1].change_list(list_type)
