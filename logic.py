import database as db
from tkinter import filedialog

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
        db.add_image(img_path)


def edit_button_callback(id):
    print(f'Editing card with ID {id}')
    