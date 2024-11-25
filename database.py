import sqlite3
from pathlib import Path
import shutil

script_directory = Path(__file__).parent
data_dir_path = script_directory/'data'
data_dir_path.mkdir(exist_ok=True)
image_dir_path = data_dir_path/'images'
image_dir_path.mkdir(exist_ok=True)

connection = sqlite3.connect(f'{data_dir_path}/cards.db')
connection.execute('PRAGMA foreign_keys = 1;')
cursor = connection.cursor()

def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS cards(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        cmc INTEGER,
                        cost TEXT,
                        card_type TEXT,
                        subtype TEXT,
                        colour TEXT,
                        rarity TEXT,
                        count INTEGER NOT NULL CHECK (count > 0),
                        img_path TEXT
                    )''')    #create table and add card parameters, 'id' parameter used as uniqe identifier
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS comments(
                        id INTEGER PRIMARY KEY,
                        comment TEXT,
                        FOREIGN KEY (id) REFERENCES cards(id)
                    )''')
    
    connection.commit()

def add_query_constructor(name, cmc, cost, card_type, subtype, colour, rarity, count, img_path): #add a card to the database
    try: 
        data_tuple = (name, cmc, cost, card_type, subtype, colour, rarity, count)
        cursor.execute('INSERT INTO cards (name, cmc, cost, card_type, subtype, colour, rarity, count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (data_tuple))
        connection.commit()
        if img_path:
            cursor.execute("SELECT id FROM cards ORDER BY id DESC")
            new_id = str(cursor.fetchone()[0])
            file_extention = img_path.split('.')[-1] if '.' in img_path else None
            new_path = str(copy_path(img_path, new_id, file_extention))
            cursor.execute('UPDATE cards SET img_path = ? WHERE id = ?', (new_path, new_id))
            connection.commit()

    except sqlite3.IntegrityError as e:
        print(f"There was an error adding the card: {e}")

def copy_path(img_path, new_id, file_extention):
    try:
        new_path = image_dir_path/(f'{new_id}.{file_extention}')
        print(new_path)
        print(img_path)
        if str(new_path) != str(img_path):
            shutil.copy(img_path, new_path)
            return new_path
        else:
            return img_path

    except sqlite3.IntegrityError as e:
        print(f'There was an error adding the image: {e}')

def edit_query_constructor(id, name=None, cmc=None, cost=None, card_type=None, subtype=None, colour=None, rarity=None, count=None, img_path=None):
    cursor.execute('SELECT 1 FROM cards WHERE id = ?', (id,)) #check if the card exists
    temp = cursor.fetchone()
    if temp is None:
        print(f'Card with id {id} not found in database.')
        return #skips the rest of the function if card is not found in the database

    update_cols = [] #update which columns?
    new_data = [] #replace with what?

    if name is not None:
        update_cols.append("name = ?")
        new_data.append(name)
    if cmc is not None:
        update_cols.append("cmc = ?")
        new_data.append(cmc)
    if cost is not None:
        update_cols.append("cost = ?")
        new_data.append(cost)
    if card_type is not None:
        update_cols.append("card_type = ?")
        new_data.append(card_type)
    if subtype is not None:
        update_cols.append("subtype = ?")
        new_data.append(subtype)
    if colour is not None:
        update_cols.append("colour = ?")
        new_data.append(colour)
    if rarity is not None:
        update_cols.append("rarity = ?")
        new_data.append(rarity)
    if count is not None:
        update_cols.append("count = ?")
        new_data.append(count)
    if img_path is not None and img_path != 'Image':
        update_cols.append("img_path = ?")
        file_extention = img_path.split('.')[-1] if '.' in img_path else None
        new_path = str(copy_path(img_path, id, file_extention))
        new_data.append(img_path)


    #proceed if there are columns to be updated
    if update_cols:
        try:
            cursor.execute(f"UPDATE cards SET {', '.join(update_cols)} WHERE id = {id}", tuple(new_data))
            connection.commit()

        except sqlite3.IntegrityError as e:
            print(f'There was an error updating the card: {e}')
    else:
        print('No parameters need updating')

def search_query_constructor(name=None, cmc=None, cost=None, card_type=None, subtype=None, colour=None, rarity=None, sort_by=None):
    search_by = []
    param = []

    match sort_by:
        case 'Date Added (New - Old)':
            order = 'id DESC'
        case 'Date Added (Old - New)':
            order = 'id ASC'
        case 'Alphabetical (A-Z)':
            order= 'name ASC'
        case 'Alphabetical (Z-A)':
            order = 'name DESC'

    if name is not None:
        search_by.append("name LIKE ?") # name LIKE used to avoid case sensitivity
        param.append(f'%{name}%') #this allows searching by only part of a card name
    if cmc is not None:
        search_by.append("cmc = ?")
        param.append(cmc)
    if cost is not None:
        search_by.append("cost LIKE ?")
        param.append(cost)
    if card_type is not None:
        search_by.append("card_type = ?")
        param.append(card_type)
    if subtype is not None:
        search_by.append("subtype LIKE ?")
        param.append(subtype)
    if colour is not None:
        search_by.append("colour = ?") # LIKE should be used as cards can have multiple colours
        param.append(colour)
    if rarity is not None:
        search_by.append("rarity = ?")
        param.append(rarity)

    if search_by:
        try:
            cursor.execute(f"SELECT * FROM cards WHERE {' AND '.join(search_by)} ORDER BY {order}", tuple(param))
            return cursor.fetchall()

        except sqlite3.IntegrityError as e:
            print(f'There was an error searching for cars {e}')

    else:
        cursor.execute(f"SELECT * FROM cards ORDER BY {order}")  
        return (cursor.fetchall())

def delete_card(id): #delete a card from the table by its id
    cursor.execute('DELETE FROM cards WHERE id = ?', (id,))
    cursor.execute('DELETE FROM images WHERE id = ?', (id,))
    connection.commit()

def fetch_by_id(id):
    cursor.execute('SELECT name, cmc, cost, card_type, subtype, colour, rarity, count, img_path FROM cards WHERE id = ?', (id,))
    row = list(cursor.fetchone())
    if row[5]:
        row[5] = tuple(row[5])
    return row

create_tables()