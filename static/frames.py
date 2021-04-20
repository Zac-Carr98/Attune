
from static.subframes import *


# abstract class for the cards that hold all other cards, used to define style and look
class LevelOneCard(ABC, tk.LabelFrame):
    def __init__(self, parent, title, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.frame_label = LevelOneLabel(self, text=title, font=(None, 20))
        self.config(bg=LEVELONE)

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
        self.frame_label.grid(row=0, column=0, columnspan=5)
        self.misc_card.grid(row=1, column=0, sticky='n', columnspan=3)
        self.abilities_card.grid(row=2, column=0, rowspan=2, sticky='n')
        self.saves_card.grid(row=2, column=1, sticky='n')
        self.skill_card.grid(row=2, column=2, sticky='n', rowspan=2)
        self.gold_card.grid(row=3, column=3)
        self.misc_features_card.grid(row=1, column=3, rowspan=2, sticky='n')


# displays most info relating to combat as inner frame
class BasicCombatCard(LevelOneCard):
    def __init__(self, parent, title, *args, **kwargs):
        LevelOneCard.__init__(self, parent, title, *args, **kwargs)

        self.ac_card = ACCard(self, "AC")
        self.init_card = InitCard(self, 'Initiative')
        self.speed_card = SpeedCard(self, 'Speed')

        self.hp_card = HitPointsCard(self, 'Hit Points')
        self.hdice_card = HitDiceCard(self, 'Hit Dice')
        self.death_card = DeathSavesCard(self, 'Death Saves')
        self.attacks_card = MiscButton(self, text='Attacks', command=self.open_item)

        self.widgets.append(self.ac_card)
        self.widgets.append(self.init_card)
        self.widgets.append(self.speed_card)
        self.widgets.append(self.hp_card)
        self.widgets.append(self.hdice_card)
        self.widgets.append(self.death_card)
        self.widgets.append(self.attacks_card)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0, columnspan=4)

        self.ac_card.grid(row=1, column=0, sticky='nsew')
        self.init_card.grid(row=1, column=1, sticky='nsew', columnspan=2)
        self.speed_card.grid(row=1, column=3, sticky='nsew')
        self.hp_card.grid(row=2, column=0, columnspan=4, sticky='ew')
        self.hdice_card.grid(row=3, column=0, sticky='ew', columnspan=2)
        self.death_card.grid(row=3, column=2, sticky='ew', columnspan=2)
        self.attacks_card.grid(row=4, column=1, columnspan=2)

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=2)

    def open_item(self):
        if not character.open_item:
            WeaponItemWindow(self, title='Attacks Menu')

            character.open_item = True


class BasicSpellcastingCard(LevelOneCard):
    def __init__(self, parent, title, *args, **kwargs):
        LevelOneCard.__init__(self, parent, title, *args, **kwargs)

        self.basics_card = SpellBasics(self, 'Spell Basics')
        self.spell_slots = SpellSlots(self, 'Spell Slots')

        self.widgets.append(self.basics_card)
        self.widgets.append(self.spell_slots)

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        self.basics_card.grid(row=1, column=0)
        self.spell_slots.grid(row=2, column=0)


# Card (frame) where all information is displayed.
# inner widgets hold most logic relating to backend
class LevelTwoCard(tk.LabelFrame, FrameTemplate, ABC):
    DICT = {}

    def __init__(self, parent, title, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        FrameTemplate.__init__(self, *args, **kwargs)
        self.config(bg=LEVELTWO)

        self.frame_label = LevelTwoLabel(self, text=title, font=(None, 17))
        self.parent = parent


# this card displays all info relating to the character at a surface level
# mainly used for information that describes the character in broad strokes
class MiscCard(LevelTwoCard):
    DICT = {'Name': 'name',
            'Class & Level': 'class_level',
            'Background': 'background',
            'Race': 'race',
            'Alignment': 'alignment',
            'Experience': 'experience',
            'Inspiration': 'inspiration',
            'Proficiency': 'proficiency'}

    def create_widgets(self, key, values):
        if values == 'proficiency':
            label = LevelTwoLabel(self, text=key)
            entry = NumberEntry(self, attr=values)
            return [label, entry]
        else:
            label = LevelTwoLabel(self, text=key)
            entry = TextEntry(self, attr=values)
            return [label, entry]

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0, columnspan=6)

        self.widgets[0][0].grid(row=1, column=0, sticky=tk.W)
        self.widgets[0][1].grid(row=1, column=1, sticky=tk.E)

        self.widgets[1][0].grid(row=1, column=2, sticky=tk.W)
        self.widgets[1][1].grid(row=1, column=3, sticky=tk.E)

        self.widgets[2][0].grid(row=1, column=4, sticky=tk.W)
        self.widgets[2][1].grid(row=1, column=5, sticky=tk.E)

        self.widgets[3][0].grid(row=2, column=0, sticky=tk.W)
        self.widgets[3][1].grid(row=2, column=1, sticky=tk.E)

        self.widgets[4][0].grid(row=2, column=2, sticky=tk.W)
        self.widgets[4][1].grid(row=2, column=3, sticky=tk.E)

        self.widgets[5][0].grid(row=2, column=4, sticky=tk.W)
        self.widgets[5][1].grid(row=2, column=5, sticky=tk.E)

        self.widgets[6][0].grid(row=3, column=0, sticky=tk.W)
        self.widgets[6][1].grid(row=3, column=1, sticky=tk.E)

        self.widgets[7][0].grid(row=3, column=2, sticky=tk.W)
        self.widgets[7][1].grid(row=3, column=3, sticky=tk.W)


# displays character's ability scores. each label and entry are generated using the LabelEntryPair widget
class AbilityCard(LevelTwoCard):
    DICT = {'Strength': 'strength',
            'Dexterity': 'dexterity',
            'Constitution': 'constitution',
            'Intelligence': 'intelligence',
            'Wisdom': 'wisdom',
            'Charisma': 'charisma'}

    def create_widgets(self, key, values):
        label = LevelTwoLabel(self, text=key)
        entry = NumberEntry(self, values, font=(None, 12))
        mod = AbilitiesMod(self, ability=values)

        return [label, entry, mod]

    def grid_items(self):
        self.inner_grid()
        # self.frame_label.grid(row=0, column=0, columnspan=3)

        row = 1
        for i in self.widgets:
            i[2].grid(row=row, column=0, pady=(15, 0), sticky='ew')
            row += 1
            i[1].grid(row=row, column=0)
            row += 1
            i[0].grid(row=row, column=0, sticky='ew')
            row += 1


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
        label = SavingMod(self, attr=values[0], ability=values[1])
        check = CustomCheckbutton(self, attr=values[0], text=key)
        return [check, label]

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0, columnspan=2)

        for index, i in enumerate(self.widgets):
            i[0].grid(row=index + 1, column=0, sticky=tk.W)
            i[1].grid(row=index + 1, column=1, sticky=tk.W)


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

    def create_widgets(self, key, values):
        label = SavingMod(self, attr=values[0], ability=values[1])
        check = CustomCheckbutton(self, attr=values[0], text=key)
        return [check, label]

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0)

        for index, i in enumerate(self.widgets):
            i[0].grid(row=index + 1, column=0, sticky=tk.W)
            i[1].grid(row=index + 1, column=1, sticky=tk.W)


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
        label = LevelTwoLabel(self, text=key)
        entry = NumberEntry(self, attr=values)
        return [label, entry]

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=4, column=0, columnspan=3)
        self.frame_label.config(font=(None, 17))

        self.widgets[0][0].grid(row=1, column=0)
        self.widgets[0][1].grid(row=0, column=0)
        self.widgets[0][1].config(font=(None, 18))
        self.widgets[1][0].grid(row=1, column=1)
        self.widgets[1][1].grid(row=0, column=1)
        self.widgets[1][1].config(font=(None, 18))
        self.widgets[2][0].grid(row=1, column=2)
        self.widgets[2][1].grid(row=0, column=2)
        self.widgets[2][1].config(font=(None, 18))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)


class HitDiceCard(LevelTwoCard):
    DICT = {'Total': 'total_dice',
            'Current': 'current_dice'}

    def create_widgets(self, key, values):
        label = LevelTwoLabel(self, text=key)
        entry = NumberEntry(self, attr=values)
        return [label, entry]

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=2, column=0, columnspan=2)

        self.widgets[0][0].grid(row=0, column=0)
        self.widgets[0][1].grid(row=0, column=1)
        self.widgets[1][0].grid(row=1, column=0)
        self.widgets[1][1].grid(row=1, column=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


class DeathSavesCard(HitDiceCard):
    DICT = {'Successes': 'success_throws',
            'Failures': 'fail_throws'}


class CombatStatCard(LevelTwoCard):
    DICT = {}

    def create_widgets(self, key, values):
        label = LevelTwoLabel(self, text=key)
        entry = NumberEntry(self, attr=values)
        return [label, entry]

    def grid_items(self):
        self.widgets[0][0].config(font=(None, 17))
        self.widgets[0][1].config(font=(None, 17))

        self.widgets[0][0].grid(row=1, column=0)
        self.widgets[0][1].grid(row=0, column=0)


class ACCard(CombatStatCard):
    DICT = {'Armor\nClass': 'armor_class'}


class InitCard(CombatStatCard):
    DICT = {'Initiative': 'initiative'}


class SpeedCard(CombatStatCard):
    DICT = {'Speed': 'speed'}


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

        self.widgets[0].grid(row=0, column=0, sticky=tk.N)
        self.widgets[1].grid(row=0, column=1)
        self.widgets[2].grid(row=0, column=0, sticky=tk.N + tk.EW)
        self.widgets[3].grid(row=1, column=0, sticky=tk.N + tk.EW)
        self.widgets[4].grid(row=2, column=0, sticky=tk.N + tk.EW)
        self.widgets[5].grid(row=3, column=0, sticky=tk.N + tk.EW)
        self.widgets[6].grid(row=4, column=0, sticky=tk.N + tk.EW)
        self.widgets[7].grid(row=5, column=0, sticky=tk.N + tk.EW)
        self.widgets[8].grid(row=6, column=0, sticky=tk.N + tk.EW)
        self.widgets[9].grid(row=7, column=0, sticky=tk.N + tk.EW)
        self.widgets[10].grid(row=8, column=0, sticky=tk.N + tk.EW)

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


class SpellBookMenu(SelectMenu):
    DICT = {'Button Holder': 'button_holder',
            'List_Box': 'list_box',
            'Cantrips': ['cantrips', 2],
            'Level One': ['1', 3],
            'Level Two': ['2', 4],
            'Level Three': ['3', 5],
            'Level Four': ['4', 6],
            'Level Five': ['5', 7],
            'Level Six': ['6', 8],
            'Level Seven': ['7', 9],
            'Level Eight': ['8', 10],
            'Level Nine': ['9', 11],
            'Add': 'add',
            }

    def create_widgets(self, key, values):
        if values == 'list_box':
            listbox = SpellsListbox(self)
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
        self.change_list('cantrips', 2)

        self.widgets[0].grid(row=0, column=0)
        self.widgets[1].grid(row=0, column=1)
        self.widgets[2].grid(row=0, column=0, sticky=tk.N + tk.EW)

        self.widgets[3].grid(row=1, column=0, sticky=tk.N + tk.EW)
        self.widgets[4].grid(row=2, column=0, sticky=tk.N + tk.EW)

        self.widgets[5].grid(row=2, column=0, sticky=tk.N + tk.EW)
        self.widgets[6].grid(row=3, column=0, sticky=tk.N + tk.EW)

        self.widgets[7].grid(row=3, column=0, sticky=tk.N + tk.EW)
        self.widgets[8].grid(row=4, column=0, sticky=tk.N + tk.EW)

        self.widgets[9].grid(row=5, column=0, sticky=tk.N + tk.EW)
        self.widgets[10].grid(row=6, column=0, sticky=tk.N + tk.EW)

        self.widgets[11].grid(row=7, column=0, sticky=tk.N + tk.EW)
        self.widgets[12].grid(row=8, column=0, sticky=tk.N + tk.EW)

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
            SpellBookWindow(self, title='Spell Book')
            character.open_spell_book = True


class SpellSlots(LevelTwoCard):
    DICT = {'Holder': 'hold',
            'Level One': 'one',
            'Level Two': 'two',
            'Level Three': 'three',
            'Level Four': 'four',
            'Level Five': 'five',
            'Level Six': 'six',
            'Level Seven': 'seven',
            'Level Eight': 'eight',
            'Level Nine': 'nine'}

    def create_widgets(self, key, values):
        if values == 'hold':
            return ButtonHolder(self)
        else:
            label = LevelTwoLabel(self.widgets[0], text=key)
            entries = SpellSlotDisplay(self.widgets[0], f'{values}_max', f'{values}_used')
            return [label, entries]

    def grid_items(self):
        self.inner_grid()
        self.frame_label.grid(row=0, column=0, columnspan=3)

        self.widgets[0].grid(row=1, column=0)
        self.widgets[1][0].grid(row=2, column=0, sticky=tk.W)
        self.widgets[1][1].grid(row=2, column=1, sticky=tk.W)
        self.widgets[2][0].grid(row=3, column=0, sticky=tk.W)
        self.widgets[2][1].grid(row=3, column=1, sticky=tk.W)
        self.widgets[3][0].grid(row=4, column=0, sticky=tk.W)
        self.widgets[3][1].grid(row=4, column=1, sticky=tk.W)
        self.widgets[4][0].grid(row=5, column=0, sticky=tk.W)
        self.widgets[4][1].grid(row=5, column=1, sticky=tk.W)
        self.widgets[5][0].grid(row=6, column=0, sticky=tk.W)
        self.widgets[5][1].grid(row=6, column=1, sticky=tk.W)
        self.widgets[6][0].grid(row=7, column=0, sticky=tk.W)
        self.widgets[6][1].grid(row=7, column=1, sticky=tk.W)
        self.widgets[7][0].grid(row=8, column=0, sticky=tk.W)
        self.widgets[7][1].grid(row=8, column=1, sticky=tk.W)
        self.widgets[8][0].grid(row=9, column=0, sticky=tk.W)
        self.widgets[8][1].grid(row=9, column=1, sticky=tk.W)
        self.widgets[9][0].grid(row=10, column=0, sticky=tk.W)
        self.widgets[9][1].grid(row=10, column=1)


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
            return MiscItemDisplay(self, list_type=self.item)
        else:
            return MiscItemDisplay(self, item=self.item)


class WeaponItemWindow(PopupWindow):
    DICT = {'Selection': 'select',
            'Display': 'display'}

    def __init__(self, parent, title, *args, **kwargs):
        PopupWindow.__init__(self, parent, title, *args, **kwargs)

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


class SpellBookWindow(PopupWindow):
    DICT = {'Selection': 'select',
            'Display': 'display'}

    def __init__(self, parent, title, list_type=None, *args, **kwargs):
        PopupWindow.__init__(self, parent, title, *args, **kwargs)

        self.list_type = list_type
        self.grid_items()

    def create_widgets(self, key, values):
        if values == 'select':
            return SpellBookMenu(self, 'Attacks')
        elif values == 'display':
            return SpellItemDisplay(self)

    def grid_items(self):
        self.inner_grid()
        self.widgets[0].grid(row=0, column=0)
        self.widgets[1].grid(row=0, column=1)

    def open_item(self, selection):
        self.widgets[1].item_mode(character.spell_items.get_item(selection))

    def add_item(self):
        self.widgets[1].add_mode()

    def on_exit(self):
        for i in self.widgets:
            i.save()
        character.open_spell_book = False
        self.parent.widgets[3].release()
        self.destroy()
