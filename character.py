from abc import ABC, abstractmethod
import database as db
import items


class Character:
    def __init__(self, db_character):
        self.id = None
        self.name = None
        self.__dict__.update(db_character)
        self.weapons = []
        self.spells = []

        self.misc_items = items.MiscItems('misc', self.id)
        self.test_add_item()

    def get_single_attr(self, attr):
        return getattr(self, attr)

    def save_single_attr(self, attr, value):
        db.save_character_attr(attr, value, self.id)

    def misc_type_list(self, list_type):
        return self.misc_items.get_item_name_list(list_type)

    def test_add_item(self):
        self.misc_items.add_item(name='Coward',
                                 description='I will runaway from things that scare me',
                                 list_type='personality')


def create_dummy():
    db.create_dummy()


def load_character(db_character):
    return Character(db_character)


def load_default():
    try:
        return load_character(db.open_default_character())
    except TypeError:
        create_dummy()
        print('Error Loading Character')
        return load_character(db.open_default_character())


character = load_default()
