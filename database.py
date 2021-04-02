import sqlite3


def init_db():
    db = get_db()

    sql_file = open("schema.sql")
    sql_as_string = sql_file.read()
    db.executescript(sql_as_string)

    print('Database Initiated')


def get_db():
    db = sqlite3.connect('instance/characters.db')
    db.row_factory = sqlite3.Row

    return db


def open_default_character():
    db = get_db()
    try:
        default_character = db.execute(
            'SELECT * FROM character'
        ).fetchone()

        return default_character

    except sqlite3.OperationalError:
        print('Error, could not find default character. Try creating a new one.')


def create_dummy():
    db = get_db()

    db.execute(
        'INSERT INTO character (name) VALUES (?)',
        ('Dummy',)
    )

    db.execute(
        'INSERT INTO misc (name, description, type, character_id) VALUES (?, ?, ?, ?)',
        ('Personality Trait', 'This is a dummy personality Trait', 'personality', 1)
    )

    db.commit()

    print('Dummy Created')


def save_character_attr(attr, value, char_id):
    db = get_db()

    db.execute(
        f'UPDATE character SET {attr}=? WHERE id=?', (value, char_id)
    )
    db.commit()


def open_item_type(item_type, char_id):
    db = get_db()

    c = db.cursor()
    c.execute(
                f'SELECT * FROM {item_type} WHERE character_id=?', (char_id,)
    )

    items = [dict(row) for row in c.fetchall()]

    return items


def insert_misc_item(item):

    db = get_db()

    db.execute(
        f'INSERT INTO misc (name, description, type, character_id) '
        f'VALUES (?, ?, ?, ?)', (item['name'], item['description'], item['type'], item['character_id'])
    )

    db.commit()


def insert_weapon_item(item):

    db = get_db()

    db.execute(
        f'INSERT INTO weapon (name, atk_bns, damage, description, type, character_id) '
        f'VALUES (?, ?, ?, ?, ?, ?)', (item['name'], item['atk_bns'], item['damage'],
                                 item['description'], item['type'], item['character_id'])
    )

    db.commit()


def update_misc_item(item):
    db = get_db()

    db.execute(
        f'UPDATE misc SET name=?, description=? WHERE id=?', (item['name'], item['description'], item['id'])
    )
    db.commit()


def update_weapon_item(item):
    db = get_db()

    db.execute(
        f'UPDATE weapon SET name=?, atk_bns=?, damage=?, description=? WHERE id=?', (item['name'], item['atk_bns'],
                                                                                   item['damage'], item['description'],
                                                                                   item['id'])
    )
    db.commit()


def delete_item(item_id, item_type):
    db = get_db()

    db.execute(
        f'DELETE FROM {item_type} WHERE id=?', (item_id,)
    )
    db.commit()
