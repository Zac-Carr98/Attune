from abc import ABC, abstractmethod
import database as db


# noinspection PyStatementEffect
class Items(ABC):
    def __init__(self, item_type, char_id):
        self.item_type = item_type
        self.items_list = db.open_item_type(item_type, char_id)
        self.to_delete = []
        self.char_id = char_id

    @abstractmethod
    def add_item(self, *args):
        pass

    @abstractmethod
    def save(self, *args):
        pass

    def delete(self, item_id):
        for i in range(len(self.items_list)):
            if self.items_list[i]['id'] == item_id:
                self.to_delete.append(self.items_list[i])
                del self.items_list[i]
                break

    def save_funct(self, command1, command2):
        for item in self.items_list:
            if item['id'] == 0:
                command1(item)
            else:
                command2(item)
        for item in self.to_delete:
            db.delete_item(item['id'], self.item_type)

    def get_item_list(self, list_type):
        item_list = []

        for item in self.items_list:
            if item['type'] == list_type:
                item_list.append(item)

        return item_list

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

    def update(self, item):
        for index, unchanged_item in enumerate(self.items_list):
            if unchanged_item['id'] == item['id']:
                self.items_list[index] = item


class MiscItems(Items):

    def add_item(self, name, description, list_type):
        if self.check_name(name):
            new_item = {'name': name, 'description': description, 'type': list_type,
                        'character_id': self.char_id, 'id': 0}
            self.items_list.append(new_item)

    def save(self):
        self.save_funct(db.insert_misc_item, db.update_misc_item)


class WeaponItems(Items):

    def add_item(self, name, atk_bns, damage, description, list_type):
        if self.check_name(name):
            new_item = {'name': name, 'atk_bns': atk_bns, 'damage': damage,
                        'description': description, 'type': list_type,
                        'character_id': self.char_id, 'id': 0}
            self.items_list.append(new_item)

    def save(self):
        self.save_funct(db.insert_weapon_item, db.update_weapon_item)
