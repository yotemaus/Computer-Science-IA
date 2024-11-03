import database as db
from tkinter import filedialog
#database
def convert_to_blob(filename): #convert image to binary data for storage in database BLOB = Binary Large
    with open(filename, 'rb') as img: #open image in binary mode
        blob_data = img.read()
    return blob_data

#gui
def card_search(name, cmc, cost, type, subtype, colour, rarity, sort_by):

    if type == "All Types":
        type = None
    if rarity == "All Rarities":
        rarity = None
    
    print(f'Searching {(name, cmc, cost, type, subtype, colour, rarity, sort_by)}')
    result = db.search_query_constructor(name, cmc, cost, type, subtype, colour, rarity, sort_by)
    return result

def image_selection():
    img_path = filedialog.askopenfilename(title='select a file: ', filetypes=[("Images", ("*.png", "*.jpg", "*.jpeg"))])
    if img_path:
        print(f"Selected file: {img_path}")

def edit_button_callback(id):
    print(f'Editing card with ID {id}')
    