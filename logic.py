import database as db
from tkinter import filedialog
#database
def convert_to_blob(filename): #convert image to binary data for storage in database BLOB = Binary Large
    with open(filename, 'rb') as img: #open image in binary mode
        blob_data = img.read()
    return blob_data

#gui
def card_search(name, cmc, cost, type, subtype, is_white, is_blue, is_black, is_red, is_green, rarity):
    colours = []
    if is_white:
        colours.append("W")
    if is_blue:
        colours.append("U")
    if is_black:
        colours.append("B")
    if is_red:
        colours.append("R")
    if is_green:
        colours.append("G")

    if type == "All Types":
        type = None
    if rarity == "All Rarities":
        rarity = None

    if colours == []:
        colours_string = None
    else:
        colours_string = ''.join(colours)

    convert_empty_str = [name, cmc, cost, subtype]
    for i in range(4):
        if convert_empty_str[i] == '':
            convert_empty_str[i] = None
    name, cmc, cost, subtype = convert_empty_str

    print(f'Searching {(name, cmc, cost, type, subtype, colours_string, rarity)}')
    result = db.search_query_constructor(name, cmc, cost, type, subtype, colours_string, rarity)
    return result

def image_selection():
    img_path = filedialog.askopenfilename(title='select a file: ', filetypes=[("Images", ("*.png", "*.jpg", "*.jpeg"))])
    if img_path:
        print(f"Selected file: {img_path}")

def edit_button_callback(id):
    print(f'Editing card with ID {id}')
    