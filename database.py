import sqlite3

# This file acts as the back-end and will be used to implement the datbase ()

connection = sqlite3.connect('data/cards.db')
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
                        count INTEGER NOT NULL CHECK (count > 0)
                    )''')    #create table and add card parameters, 'id' parameter used as uniqe identifier
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS images(
                        id INTEGER PRIMARY KEY,
                        image BLOB,
                        FOREIGN KEY (id) REFERENCES cards(id)
                    )''') #images will be stored in a separate table using a foreign key to make fetchall() more efficient
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS comments(
                        id INTEGER PRIMARY KEY,
                        comment TEXT,
                        FOREIGN KEY (id) REFERENCES cards(id)
                    )''')
    
    connection.commit()

def convert_to_blob(filename): #convert image to binary data for storage in database BLOB = Binary Large
    with open(filename, 'rb') as img: #open image in binary mode
        blob_data = img.read()
    return blob_data 

def add_card(name, cmc, cost, card_type, subtype, colour, rarity, count): #add a card to the database
    try: 
        data_tuple = (name, cmc, cost, card_type, subtype, colour, rarity, count) 
        cursor.execute('INSERT INTO cards (name, cmc, cost, card_type, subtype, colour, rarity, count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (data_tuple))
        connection.commit()

    except sqlite3.IntegrityError as e:
        print(f"There was an error adding the card: {e}")

def add_image(id, image):
    try:
        blob_data = convert_to_blob(f'data/images/{image}')
        cursor.execute('INSERT INTO IMAGES (id, image) VALUES (?, ?)', (id, blob_data))
        connection.commit()

    except sqlite3.IntegrityError as e:
        print(f'There was an error adding the image: {e}')

def edit_card_param(id, name=None, cmc=None, cost=None, card_type=None, subtype=None, colour=None, rarity=None, count=None):
    cursor.execute('SELECT 1 FROM cards WHERE id = ?', (id,)) #check if the card exists
    if cursor.fetchone() is None:
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

    #proceed if there are columns to be updated
    if update_cols:
        try:
            cursor.execute(f"UPDATE cards SET {', '.join(update_cols)} WHERE id = {id}", tuple(new_data))
            connection.commit()

        except sqlite3.IntegrityError as e:
            print(f'There was an error updating the card: {e}')
    else:
        print('No parameters need updating')

def edit_image(id, image): #swap image with new path
    cursor.execute('SELECT 1 FROM imaged WHERE id = ?', (id,))
    if cursor.fetchone() is None:
        print(f'Image with card id {id} not found in database.')
        return
    
    try:
        blob_data = convert_to_blob(image)
        cursor.execute('UPDATE images SET image = ? WHERE id ?', (blob_data, id))
        connection.commit()

    except sqlite3.IntegrityError as e:
        print(f"There was an error updating the image {e}")

def search_query_constructor(name=None, cmc=None, cost=None, card_type=None, subtype=None, colour=None, rarity=None):
    search_by = []
    param = []

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

            cursor.execute(f"SELECT * FROM cards WHERE {' AND '.join(search_by)}", tuple(param))
            return cursor.fetchall()

        except sqlite3.IntegrityError as e:
            print(f'There was an error searching for cars {e}')

    else:
        cursor.execute("SELECT * FROM cards")  
        return (cursor.fetchall())

def delete_card(id): #delete a card from the table by its id
    cursor.execute('DELETE FROM cards WHERE id = ?', (id,))
    cursor.execute('DELETE FROM images WHERE id = ?', (id,))
    connection.commit()


# cursor.execute('DROP TABLE cards')
# cursor.execute('DROP TABLE images')

# print(search(name = 'i'))

# create_tables()