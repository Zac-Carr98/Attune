from abc import ABC, abstractmethod
import database as db


class Items(ABC):
    def __init__(self, item_type, char_id):
        self.items_list = db.open_item_type(item_type, char_id)
        self.orig_list = self.items_list
        self.char_id = char_id

    @abstractmethod
    def get_item_name_list(self, *args):
        pass

    @abstractmethod
    def add_item(self, *args):
        pass

    @abstractmethod
    def save(self, *args):
        pass

    def check_name(self, name):
        for item in self.items_list:
            if item['name'] == name:
                print('Error, this item name already exists')
                return False
        return True

    def get_item(self, name):
        for item in self.items_list:
            if item['name'] == name:
                return item


class MiscItems(Items):

    def get_item_name_list(self, list_type):
        item_name_list = []

        for item in self.items_list:
            if item['type'] == list_type:
                item_name_list.append(item['name'])

        return item_name_list

    def add_item(self, name, description, list_type):
        if self.check_name(name):
            new_item = {'name': name, 'description': description, 'type': list_type,
                        'character_id': self.char_id, 'id': 0}
            self.items_list.append(new_item)

    def update(self, item):
        for index, unchanged_item in enumerate(self.items_list):
            if unchanged_item['id'] == item['id']:
                self.items_list[index] = item

    def save(self):
        for item in self.items_list:
            if item['id'] == 0:
                db.insert_misc_item(item)
            else:
                db.update_misc_item(item)
