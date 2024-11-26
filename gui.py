import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import database as db
import api_handler as api

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Database Manager")
app.geometry("1200x700")

#search bar and add button
title = ctk.CTkLabel(app, text='Your Cards', font=('Helvetica', 36, 'bold'), text_color='white')
title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky='w')

add_button = ctk.CTkButton(app, text='+', command=lambda: add_card_window())
add_button.grid(row=0, column=5, padx=(5, 20), pady=(20, 0), sticky='ew')

namesearch = ctk.CTkEntry(app, placeholder_text='Search by Card Name')
namesearch.grid(row=1, column=0, columnspan=5, padx=(20, 5), pady=10, sticky='ew')

searchbutton = ctk.CTkButton(app, text='Search', command=lambda: init_search()) #lambda is used to pass parameters to a function
searchbutton.grid(row=1, column=5, padx=(5, 20), pady=10, sticky='ew')

# filter frames
cost_frame = ctk.CTkFrame(app, height=20)
cost_frame.grid(row=3, column=0, padx=(20, 5), pady=(10,5), sticky='ew')
cost_frame.grid_columnconfigure(0, weight=1)

cmc_frame = ctk.CTkFrame(app, height=20)
cmc_frame.grid(row=3, column=1, padx=5, pady=(10,5), sticky='ew')
cmc_frame.grid_columnconfigure(0, weight=1)

type_frame = ctk.CTkFrame(app, height=20)
type_frame.grid(row=3, column=2, padx=5, pady=(10,5), sticky='ew')
type_frame.grid_columnconfigure(0, weight=1)

subtype_frame = ctk.CTkFrame(app, height=20)
subtype_frame.grid(row=3, column=3, padx=5, pady=(10,5), sticky='ew')
subtype_frame.grid_columnconfigure(0, weight=1)

colour_frame = ctk.CTkFrame(app, height=20)
colour_frame.grid(row=3, column=4, padx=5, pady=(10,5), sticky='ew')
colour_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

rarity_frame = ctk.CTkFrame(app, height=20)
rarity_frame.grid(row=3, column=5, padx=(5, 20), pady=(10,5), sticky='ew')
rarity_frame.grid_columnconfigure(0, weight=1)


#cost filter
cost_filter_label = ctk.CTkLabel(cost_frame, text='Cost', font=('Helvetica', 12, 'bold'), text_color='white')
cost_filter_label.grid(column=0, row=0, padx=5, sticky='w')

cost_filter = ctk.CTkEntry(cost_frame, placeholder_text='Example: 2RR')
cost_filter.grid(column=0, row=1, padx=5, pady=(0, 5), sticky='ew')


#cmc filter
cmc_filter_label = ctk.CTkLabel(cmc_frame, text='Converted Cost', font=('Helvetica', 12, 'bold'), text_color='white')
cmc_filter_label.grid(column=0, row=0, padx=5, sticky='w')

cmc_filter = ctk.CTkEntry(cmc_frame, placeholder_text='Example: 4')
cmc_filter.grid(column=0, row=1, padx=5, pady=(0, 5), sticky='ew')


#type filter
type_filter_label = ctk.CTkLabel(type_frame, text='Card Type', font=('Helvetica', 12, 'bold'), text_color='white')
type_filter_label.grid(column=0, row=0, padx=5, sticky='w')

type_filter = ctk.CTkComboBox(type_frame, values=['All Types','Instant','Sorcery','Artifact','Creature','Enchantment','Land','Planeswalker'])
type_filter.grid(column=0, row=1, padx=5, pady=(0, 5), sticky='ew')


#subtype filter
subtype_filter_label = ctk.CTkLabel(subtype_frame, text='Subtype', font=('Helvetica', 12, 'bold'), text_color='white')
subtype_filter_label.grid(column=0, row=0, padx=5, sticky='w')

subtype_filter = ctk.CTkEntry(subtype_frame, placeholder_text='Example: Dragon')
subtype_filter.grid(column=0, row=1, padx=5, pady=(0, 5), sticky='ew')


#colour filter
colour_filter_label = ctk.CTkLabel(colour_frame, text='Colour', font=('Helvetica', 12, 'bold'), text_color='white')
colour_filter_label.grid(column=0, row=0, padx=5, sticky='w')

colour_checkbox_w = ctk.CTkCheckBox(colour_frame, width=50, text=('W'))
colour_checkbox_w.grid(column=0, row=1, padx=(5, 0), pady=(0, 8), sticky='ew')
colour_checkbox_u = ctk.CTkCheckBox(colour_frame, width=50, text=('U'))
colour_checkbox_u.grid(column=1, row=1, pady=(0, 8), sticky='ew')
colour_checkbox_b = ctk.CTkCheckBox(colour_frame, width=50, text=('B'))
colour_checkbox_b.grid(column=2, row=1, pady=(0, 8), sticky='ew')
colour_checkbox_r = ctk.CTkCheckBox(colour_frame, width=50, text=('R'))
colour_checkbox_r.grid(column=3, row=1, pady=(0, 8), sticky='ew')
colour_checkbox_g = ctk.CTkCheckBox(colour_frame, width=45, text=('G'))
colour_checkbox_g.grid(column=4, row=1, padx=(0, 5), pady=(0, 8), sticky='ew')


#rarity filter
rarity_filter_label = ctk.CTkLabel(rarity_frame, text='Rarity', font=('Helvetica', 12, 'bold'), text_color='white')
rarity_filter_label.grid(column=0, row=0, padx=5, sticky='w')

rarity_filter = ctk.CTkComboBox(rarity_frame, values=['All Rarities','Common','Uncommon','Rare','Mythic Rare'])
rarity_filter.grid(column=0, row=1, padx=5, pady=(0, 5), sticky='ew')


#sort by
sort_by_frame = ctk.CTkFrame(app)
sort_by_frame.grid_columnconfigure((0, 1, 2), weight=1)
sort_by_frame.grid(column=0, columnspan=2, row=4, padx=(20, 5), pady=5, sticky='ew')
sort_by_label = ctk.CTkLabel(sort_by_frame, text='Sort By:', font=('Helvetica', 16, 'bold'), text_color='white')
sort_by_label.grid(column=0, row=0, padx=5, pady=5, sticky='ew')
sort_by_dropdown = ctk.CTkOptionMenu(sort_by_frame, values=['Date Added (New - Old)', 'Date Added (Old - New)', 'Alphabetical (A-Z)', 'Alphabetical (Z-A)'])
sort_by_dropdown.grid(column=1, columnspan=2, row=0, padx=(0, 5), pady=5, sticky='ew')

#grid/list
view_option = ctk.CTkTabview(app)
view_option.grid(row=5, column=0, columnspan=6, padx=40, pady=10, sticky='nesw')
list = view_option.add("List View")
grid = view_option.add("Grid View")
list.grid_columnconfigure(0, weight=1)
list.grid_rowconfigure(0, weight=1)
grid.grid_columnconfigure(0, weight=1)
grid.grid_rowconfigure(0, weight=1)


#card display window for list view
list_scroll = ctk.CTkScrollableFrame(list)
list_scroll.grid(row=0, column=0, sticky='nesw')
list_scroll.grid_columnconfigure(0, weight=1)

#card display window for grid view
grid_scroll = ctk.CTkScrollableFrame(grid)
grid_scroll.grid(row=0, column=0, sticky='nesw')
grid_scroll.grid_columnconfigure((0, 1, 2, 3), weight=1)

#the window to add a card
def add_card_window():
    add_window = ctk.CTkToplevel()
    add_window.geometry('430x1030')
    add_window.grid_columnconfigure(0, weight=1)
    add_window.title('Add a Card')

    add_api_frame = ctk.CTkFrame(add_window)
    add_api_frame.grid(row=0, column=0, padx=10, pady=(10,5), sticky='ew')
    add_api_frame.grid_columnconfigure(0, weight=1)
    search_api_entry = ctk.CTkEntry(add_api_frame, placeholder_text='Enter Card Name')
    search_api_entry.grid(row=0, column=0, padx=(5,0), pady=(10,5), sticky='ew')
    select_fill_option = ctk.CTkOptionMenu(add_api_frame, state='disabled', values=['Select'])
    select_fill_option.grid(row=1, column=0, padx=(5,0), pady=(5,10), sticky='ew')
    search_api_button = ctk.CTkButton(add_api_frame, text='Search Scryfall', fg_color='purple', command=lambda: 
                                                                                                select_fill_option.configure(
                                                                                                values=api.match_name(search_api_entry.get()),
                                                                                                state='enabled'
                                                                                                ))
    search_api_button.grid(row=0, column=1, padx=5, pady=(10,5), sticky='ew')
    fill_button = ctk.CTkButton(add_api_frame, text='Fill', command=lambda: fill_add_fields(add_name_entry, add_cost_entry, add_cmc_entry, add_type_entry,
                                                                            add_subtype_entry, add_colour_checkbox_w, add_colour_checkbox_u,
                                                                            add_colour_checkbox_b, add_colour_checkbox_r, add_colour_checkbox_g,
                                                                            add_rarity_entry, add_count_entry, add_image_label, select_fill_option))
    fill_button.grid(row=1, column=1, padx=5, pady=(5,10), sticky='ew')

    add_name_frame = ctk.CTkFrame(add_window)
    add_name_frame.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
    add_name_frame.grid_columnconfigure(0, weight=1)
    add_name_label = ctk.CTkLabel(add_name_frame, text='Card Name', font=('Helvetica', 12, 'bold'), text_color='white')
    add_name_label.grid(column=0, row=0, padx=5, sticky='w')
    add_name_entry = ctk.CTkEntry(add_name_frame)
    add_name_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')

    add_cost_frame = ctk.CTkFrame(add_window)
    add_cost_frame.grid(row=2, column=0, padx=10, pady=5, sticky='ew')
    add_cost_frame.grid_columnconfigure(0, weight=1)
    add_cost_label = ctk.CTkLabel(add_cost_frame, text='Cost (as it appears on the card)', font=('Helvetica', 12, 'bold'), text_color='white')
    add_cost_label.grid(column=0, row=0, padx=5, sticky='w')
    add_cost_entry= ctk.CTkEntry(add_cost_frame)
    add_cost_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')

    add_cmc_frame = ctk.CTkFrame(add_window)
    add_cmc_frame.grid(row=3, column=0, padx=10, pady=5, sticky='ew')
    add_cmc_frame.grid_columnconfigure(0, weight=1)
    add_cmc_label = ctk.CTkLabel(add_cmc_frame, text='Converted Mana Cost', font=('Helvetica', 12, 'bold'), text_color='white')
    add_cmc_label.grid(column=0, row=0, padx=5, sticky='w')
    add_cmc_entry= ctk.CTkEntry(add_cmc_frame)
    add_cmc_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')

    add_type_frame = ctk.CTkFrame(add_window)
    add_type_frame.grid(row=4, column=0, padx=10, pady=5, sticky='ew')
    add_type_frame.grid_columnconfigure(0, weight=1)
    add_type_label = ctk.CTkLabel(add_type_frame, text='Card Type', font=('Helvetica', 12, 'bold'), text_color='white')
    add_type_label.grid(column=0, row=0, padx=5, sticky='w')
    add_type_entry = ctk.CTkComboBox(add_type_frame, values=['Instant','Sorcery','Artifact','Creature','Enchantment','Land','Planeswalker'])
    add_type_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')
    
    add_subtype_frame = ctk.CTkFrame(add_window)
    add_subtype_frame.grid(row=5, column=0, padx=10, pady=5, sticky='ew')
    add_subtype_frame.grid_columnconfigure(0, weight=1)
    add_subtype_label = ctk.CTkLabel(add_subtype_frame, text='Subtype', font=('Helvetica', 12, 'bold'), text_color='white')
    add_subtype_label.grid(column=0, row=0, padx=5, sticky='w')
    add_subtype_entry = ctk.CTkEntry(add_subtype_frame)
    add_subtype_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')

    add_colours_frame = ctk.CTkFrame(add_window)
    add_colours_frame.grid(row=6, column=0, padx=10, pady=5, sticky='ew')
    add_colours_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
    add_colours_label = ctk.CTkLabel(add_colours_frame, text='Colour', font=('Helvetica', 12, 'bold'), text_color='white')
    add_colours_label.grid(column=0, row=0, padx=5, sticky='w')
    add_colour_checkbox_w = ctk.CTkCheckBox(add_colours_frame, width=50, text=('W'))
    add_colour_checkbox_w.grid(column=0, row=1, padx=(5, 0), pady=(0, 8), sticky='ew')
    add_colour_checkbox_u = ctk.CTkCheckBox(add_colours_frame, width=50, text=('U'))
    add_colour_checkbox_u.grid(column=1, row=1, pady=(0, 8), sticky='ew')
    add_colour_checkbox_b = ctk.CTkCheckBox(add_colours_frame, width=50, text=('B'))
    add_colour_checkbox_b.grid(column=2, row=1, pady=(0, 8), sticky='ew')
    add_colour_checkbox_r = ctk.CTkCheckBox(add_colours_frame, width=50, text=('R'))
    add_colour_checkbox_r.grid(column=3, row=1, pady=(0, 8), sticky='ew')
    add_colour_checkbox_g = ctk.CTkCheckBox(add_colours_frame, width=45, text=('G'))
    add_colour_checkbox_g.grid(column=4, row=1, padx=(0, 5), pady=(0, 8), sticky='ew')

    add_rarity_frame = ctk.CTkFrame(add_window)
    add_rarity_frame.grid(row=7, column=0, padx=10, pady=5, sticky='ew')
    add_rarity_frame.grid_columnconfigure(0, weight=1)
    add_rarity_label = ctk.CTkLabel(add_rarity_frame, text='Rarity', font=('Helvetica', 12, 'bold'), text_color='white')
    add_rarity_label.grid(column=0, row=0, padx=5, sticky='w')
    add_rarity_entry = ctk.CTkComboBox(add_rarity_frame, values=['Common','Uncommon','Rare','Mythic Rare'])
    add_rarity_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')

    add_count_frame = ctk.CTkFrame(add_window)
    add_count_frame.grid(row=8, column=0, padx=10, pady=5, sticky='ew')
    add_count_frame.grid_columnconfigure(0, weight=1)
    add_count_label = ctk.CTkLabel(add_count_frame, text='Quantity (Enter an Integer)', font=('Helvetica', 12, 'bold'), text_color='white')
    add_count_label.grid(column=0, row=0, padx=5, sticky='w')
    add_count_entry = ctk.CTkEntry(add_count_frame)
    add_count_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')

    add_image_frame = ctk.CTkFrame(add_window)
    add_image_frame.grid(row=9, column=0, padx=10, pady=5, sticky='ew')
    add_image_frame.grid_columnconfigure(0, weight=1)
    add_image_label = ctk.CTkLabel(add_image_frame, text='Image', font=('Helvetica', 12, 'bold'), text_color='white')
    add_image_label.grid(column=0, row=0, padx=5, sticky='w')
    add_image_button = ctk.CTkButton(add_image_frame, text='Select a File', command=lambda: add_image_label.configure(text=image_selection()))
    add_image_button.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')


    confirm_add_button = ctk.CTkButton(add_window, text='Add', command=lambda: [init_add(add_name_entry, add_cost_entry, add_cmc_entry, add_type_entry,
                                                                                        add_subtype_entry, add_colour_checkbox_w, add_colour_checkbox_u,
                                                                                        add_colour_checkbox_b, add_colour_checkbox_r, add_colour_checkbox_g,
                                                                                        add_rarity_entry, add_count_entry, add_image_label), 
                                                                                add_window.destroy(), 
                                                                                init_search()])
    confirm_add_button.grid(row=10, column=0, padx=10, pady=(5,10), sticky='nesw')
    add_window.grid_rowconfigure(10, weight=1)

def fill_add_fields(add_name_entry, add_cost_entry, add_cmc_entry, add_type_entry,
            add_subtype_entry, add_colour_checkbox_w, add_colour_checkbox_u,
            add_colour_checkbox_b, add_colour_checkbox_r, add_colour_checkbox_g,
            add_rarity_entry, add_count_entry, add_image_label, select_fill_option):
    
    cardname = select_fill_option.get()
    data = api.search_card(cardname)

    namevar = ctk.StringVar(value=data['name']) # type: ignore
    add_name_entry.configure(textvariable=namevar)

    costvar = ctk.StringVar(value=data['cost']) # type: ignore
    add_cost_entry.configure(textvariable=costvar)

    cmcvar = ctk.StringVar(value=data['cmc']) # type: ignore
    add_cmc_entry.configure(textvariable=cmcvar)

    add_type_entry.set(data['card_type']) # type: ignore

    subtypevar = ctk.StringVar(value=data['subtype']) # type: ignore
    add_subtype_entry.configure(textvariable=subtypevar)

    colours = data['colors'] # type: ignore
    add_colour_checkbox_w.deselect()
    add_colour_checkbox_u.deselect()
    add_colour_checkbox_b.deselect()
    add_colour_checkbox_r.deselect()
    add_colour_checkbox_g.deselect()
    if 'W' in colours:
        add_colour_checkbox_w.select()
    if 'U' in colours:
        add_colour_checkbox_u.select()
    if 'B' in colours:
        add_colour_checkbox_b.select()
    if 'R' in colours:
        add_colour_checkbox_r.select()
    if 'G' in colours:
        add_colour_checkbox_g.select()

    add_rarity_entry.set(data['rarity']) # type: ignore

    countvar = ctk.StringVar(value='1')
    add_count_entry.configure(textvariable=countvar)


#passing parameters to the databse add function
def init_add(add_name_entry, add_cost_entry, add_cmc_entry, add_type_entry,
            add_subtype_entry, add_colour_checkbox_w, add_colour_checkbox_u,
            add_colour_checkbox_b, add_colour_checkbox_r, add_colour_checkbox_g,
            add_rarity_entry, add_count_entry, add_image_label):
    add_data = {
        'name' : add_name_entry.get(),
        'cost' : add_cost_entry.get(),
        'cmc' : add_cmc_entry.get(),
        'card_type' : add_type_entry.get(),
        'subtype' : add_subtype_entry.get(),
        'colour' : [
            'W' if add_colour_checkbox_w.get() else '',
            'U' if add_colour_checkbox_u.get() else '',
            'B' if add_colour_checkbox_b.get() else '',
            'R' if add_colour_checkbox_r.get() else '',
            'G' if add_colour_checkbox_g.get() else ''
        ],
        'rarity' : add_rarity_entry.get(),
        'count' : add_count_entry.get(),
        'img_path' : add_image_label.cget('text')
    }

    #remove empty strings from colour information 
    add_data['colour'] = [color for color in add_data['colour'] if color]
    add_data['colour'] = ''.join(add_data['colour'])
    add_data['img_path'] = None if add_data == 'Image' else add_data['img_path']

    #merge colour values into a string
    add_data = {key: (value if value !='' else None) for key, value in add_data.items()}
    db.add_query_constructor(**add_data)

#take name and filter settings from search bar and call display with search results
def init_search():
    search_data = {
    'name' : namesearch.get(),
    'cmc' : cmc_filter.get(),
    'cost' : cost_filter.get(),
    'card_type' : type_filter.get(),
    'subtype' : subtype_filter.get(),
    'colour' : [
        'W' if colour_checkbox_w.get() else '',
        'U' if colour_checkbox_u.get() else '',
        'B' if colour_checkbox_b.get() else '',
        'R' if colour_checkbox_r.get() else '',
        'G' if colour_checkbox_g.get() else '',
        ],
    'rarity' : rarity_filter.get(),
    'sort_by' : sort_by_dropdown.get()
    }

    search_data['colour'] = [color for color in search_data['colour'] if color]
    search_data['colour'] = ''.join(search_data['colour'])
    search_data['card_type'] = None if search_data['card_type'] == 'All Types' else search_data['card_type']
    search_data['rarity'] = None if search_data['rarity'] == 'All Rarities' else search_data['rarity']
    search_data = {key: (None if value == '' else value) for key, value in search_data.items()}


    print(f'Searching: {search_data}')
    results = db.search_query_constructor(**search_data)

    print(f'Results {results}')
    display_results(results)

def clear_results():
    for widget in list_scroll.winfo_children():
        widget.destroy()
    for widget in grid_scroll.winfo_children():
        widget.destroy()

def dlist(results):
        for i, row in enumerate(results):
            id, name, cmc, cost, type, subtype, colour, rarity, count, _ = [
                        "N/A" if value is None else value for value in row
                    ]
            
            list_card_frame = ctk.CTkFrame(list_scroll, fg_color='#363636')
            list_card_frame.grid(row=i, column=0, pady=0, sticky='new')
            list_card_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)  # Distribute column weight

            # Name Frame (list)
            name_frame_display = ctk.CTkFrame(list_card_frame)
            name_frame_display.grid(row=0, column=0, padx=(5, 2.5), pady=5, sticky='ew')  # remove padding  around frame
            name_frame_display.grid_columnconfigure(0, weight=1) #alligns the text in the center of each frame
            name_label = ctk.CTkLabel(name_frame_display, text=name, font=('Helvetica', 14, 'bold'))
            name_label.grid(row=0, column=0, padx=5, pady=0, sticky='ew')  # Ensure no padding for the label

            #Mana Cost Frame (list)
            cost_frame_display = ctk.CTkFrame(list_card_frame)
            cost_frame_display.grid(row=0, column=1, padx=2.5, pady=5, sticky='ew')
            cost_frame_display.grid_columnconfigure(0, weight=1)  
            cost_label = ctk.CTkLabel(cost_frame_display, text=f'Cost: {cost}', font=('Helvetica', 14, 'bold'))
            cost_label.grid(row=0, column=0, padx=5, pady=0, sticky='ew')

            #CMC Frame (list)
            cmc_frame_display = ctk.CTkFrame(list_card_frame)
            cmc_frame_display.grid(row=0, column=2, padx=2.5, pady=5, sticky='ew')
            cmc_frame_display.grid_columnconfigure(0, weight=1)
            cmc_label = ctk.CTkLabel(cmc_frame_display, text=f'CMC: {cmc}', font=('Helvetica', 14, 'bold'))
            cmc_label.grid(row=0, column=0, padx=5, pady=0, sticky='ew')

            # Type Frame (list)
            type_frame_display = ctk.CTkFrame(list_card_frame)
            type_frame_display.grid(row=0, column=3, padx=2.5, pady=5, sticky='ew')
            type_frame_display.grid_columnconfigure(0, weight=1)  
            type_label = ctk.CTkLabel(type_frame_display, text=type, font=('Helvetica', 14, 'bold'))
            type_label.grid(row=0, column=0, padx=5, pady=0, sticky='ew')

            # Subtype Frame (list)
            subtype_frame_display = ctk.CTkFrame(list_card_frame)
            subtype_frame_display.grid(row=0, column=4, padx=2.5, pady=5, sticky='ew')
            subtype_frame_display.grid_columnconfigure(0, weight=1) 
            subtype_label = ctk.CTkLabel(subtype_frame_display, text=subtype, font=('Helvetica', 14, 'bold'))
            subtype_label.grid(row=0, column=0, padx=5, pady=0, sticky='ew')

            # Colour Frame (list)
            colour_frame_display = ctk.CTkFrame(list_card_frame)
            colour_frame_display.grid(row=0, column=5, padx=2.5, pady=5, sticky='ew')
            colour_frame_display.grid_columnconfigure(0, weight=1) 
            colour_label = ctk.CTkLabel(colour_frame_display, text=colour, font=('Helvetica', 14, 'bold'))
            colour_label.grid(row=0, column=0, padx=5, pady=0, sticky='ew')

            # Rarity Frame (list)
            rarity_frame_display = ctk.CTkFrame(list_card_frame)
            rarity_frame_display.grid(row=0, column=6, padx=2.5, pady=5, sticky='ew')
            rarity_frame_display.grid_columnconfigure(0, weight=1) 
            rarity_label = ctk.CTkLabel(rarity_frame_display, text=rarity, font=('Helvetica', 14, 'bold'))
            rarity_label.grid(row=0, column=0, padx=5, pady=0, sticky='ew')

            # Count Frame (list)
            count_frame_display = ctk.CTkFrame(list_card_frame)
            count_frame_display.grid(row=0, column=7, padx=2.5, pady=5, sticky='ew')
            count_frame_display.grid_columnconfigure(0, weight=1) 
            count_label = ctk.CTkLabel(count_frame_display, text=f"Quantity: {count}", font=('Helvetica', 14, 'bold'))
            count_label.grid(row=0, column=0, padx=5, pady=0, sticky='ew')
            
            # Edit Button (list)
            edit_button = ctk.CTkButton(list_card_frame, text='Edit', width=40, command=lambda id=id: edit_window(id)) #the lambda function is used to remember the id for ediitng
            edit_button.grid(row=0, column=8, padx=(0, 5), pady=5, sticky='e')

def dgrid(results):
    for i, row in enumerate(results):

        id, name, cmc, cost, type, subtype, colour, rarity, count, img_path = [
                    "N/A" if value is None else value for value in row
                ]
        print(name)
        grid_card_frame = ctk.CTkFrame(grid_scroll, fg_color='#363636')
        grid_card_frame.grid(row=i // 4, column=i % 4, pady=5, padx=5, sticky='ew')
        grid_card_frame.grid_columnconfigure((0, 1, 2), weight=1)

        if img_path != "N/A":
            image = Image.open(img_path)
            card_image = ctk.CTkImage(image, size=(250, 350))

            image_display = ctk.CTkLabel(grid_card_frame, image=card_image, text='')
            image_display.grid(row=0, column=0, columnspan=3, pady=(5,0), padx=5, sticky='ew')

        grid_name_frame = ctk.CTkFrame(grid_card_frame)
        grid_name_frame.grid(row=2, column=0, padx=5, pady=(4, 5), sticky='ew')
        grid_name_label = ctk.CTkLabel(grid_name_frame, text=name, font=('Helvetica', 14, 'bold'))
        grid_name_label.grid(row=0, column=0, padx=5, sticky='w')

        grid_count_frame = ctk.CTkFrame(grid_card_frame)
        grid_count_frame.grid(row=2, column=1, pady=(4, 5), sticky='w')
        grid_count_label = ctk.CTkLabel(grid_count_frame, text=count)
        grid_count_label.grid(row=0, column=0, padx=5, sticky='ew')

        edit_button = ctk.CTkButton(grid_card_frame, text='Edit', width=40, command=lambda id=id: edit_window(id)) #the lambda function is used to remember the id for ediitng
        edit_button.grid(row=2, column=2, padx=(0, 5), pady=(2, 5), sticky='e')
    placeholders(i+1)

def placeholders(shown): #to maintain the grids structure
    if shown % 4 != 0:
        count = 4 - shown % 4
        current_row = shown // 4
        start_col = shown % 4
        for i in range(count):
            grid_card_frame = ctk.CTkFrame(grid_scroll, width=260, height=390)
            grid_card_frame.grid(row=current_row, column=start_col+i, pady=5, padx=5, sticky='ew')


#card display frames inside scrollable window
def display_results(results): #results is a list of tuples passed by the card search function
    clear_results()
    dlist(results)
    dgrid(results)

            
def edit_window(id):
    data = db.fetch_by_id(id)
    print(data)
    name, cmc, cost, type, subtype, colours, rarity, count, img_path = ['' if value is None else str(value) for value in data]

    edit_window = ctk.CTkToplevel()
    edit_window.geometry('430x730')
    edit_window.grid_columnconfigure((0,1), weight=1)
    edit_window.title(f'Editing {name}')

    edit_name_frame = ctk.CTkFrame(edit_window)
    edit_name_frame.grid(row=0, column=0, padx=10, pady=(10,5), sticky='ew', columnspan=2)
    edit_name_frame.grid_columnconfigure(0, weight=1)
    edit_name_label = ctk.CTkLabel(edit_name_frame, text='Card Name', font=('Helvetica', 12, 'bold'), text_color='white')
    edit_name_label.grid(column=0, row=0, padx=5, sticky='w')
    edit_name_entry = ctk.CTkEntry(edit_name_frame)
    edit_name_entry.insert(0, name)
    edit_name_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')

    edit_cost_frame = ctk.CTkFrame(edit_window)
    edit_cost_frame.grid(row=1, column=0, padx=10, pady=5, sticky='ew', columnspan=2)
    edit_cost_frame.grid_columnconfigure(0, weight=1)
    edit_cost_label = ctk.CTkLabel(edit_cost_frame, text='Cost (as it appears on the card)', font=('Helvetica', 12, 'bold'), text_color='white')
    edit_cost_label.grid(column=0, row=0, padx=5, sticky='w')
    edit_cost_entry = ctk.CTkEntry(edit_cost_frame)
    edit_cost_entry.insert(0, cost)
    edit_cost_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')

    edit_cmc_frame = ctk.CTkFrame(edit_window)
    edit_cmc_frame.grid(row=2, column=0, padx=10, pady=5, sticky='ew', columnspan=2)
    edit_cmc_frame.grid_columnconfigure(0, weight=1)
    edit_cmc_label = ctk.CTkLabel(edit_cmc_frame, text='Converted Mana Cost', font=('Helvetica', 12, 'bold'), text_color='white')
    edit_cmc_label.grid(column=0, row=0, padx=5, sticky='w')
    edit_cmc_entry = ctk.CTkEntry(edit_cmc_frame)
    edit_cmc_entry.insert(0, cmc)
    edit_cmc_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')

    edit_type_frame = ctk.CTkFrame(edit_window)
    edit_type_frame.grid(row=3, column=0, padx=10, pady=5, sticky='ew', columnspan=2)
    edit_type_frame.grid_columnconfigure(0, weight=1)
    edit_type_label = ctk.CTkLabel(edit_type_frame, text='Card Type', font=('Helvetica', 12, 'bold'), text_color='white')
    edit_type_label.grid(column=0, row=0, padx=5, sticky='w')
    edit_type_entry = ctk.CTkComboBox(edit_type_frame, values=['Instant','Sorcery','Artifact','Creature','Enchantment','Land','Planeswalker'])
    edit_type_entry.set(type)
    edit_type_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')
    
    edit_subtype_frame = ctk.CTkFrame(edit_window)
    edit_subtype_frame.grid(row=4, column=0, padx=10, pady=5, sticky='ew', columnspan=2)
    edit_subtype_frame.grid_columnconfigure(0, weight=1)
    edit_subtype_label = ctk.CTkLabel(edit_subtype_frame, text='Subtype', font=('Helvetica', 12, 'bold'), text_color='white')
    edit_subtype_label.grid(column=0, row=0, padx=5, sticky='w')
    edit_subtype_entry = ctk.CTkEntry(edit_subtype_frame)
    edit_subtype_entry.insert(0, subtype)
    edit_subtype_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')

    edit_colours_frame = ctk.CTkFrame(edit_window)
    edit_colours_frame.grid(row=5, column=0, padx=10, pady=5, sticky='ew', columnspan=2)
    edit_colours_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
    edit_colours_label = ctk.CTkLabel(edit_colours_frame, text='Colour', font=('Helvetica', 12, 'bold'), text_color='white')
    edit_colours_label.grid(column=0, row=0, padx=5, sticky='w')
    edit_colour_checkbox_w = ctk.CTkCheckBox(edit_colours_frame, width=50, text=('W'))
    edit_colour_checkbox_w.grid(column=0, row=1, padx=(5, 0), pady=(0, 8), sticky='ew')
    edit_colour_checkbox_u = ctk.CTkCheckBox(edit_colours_frame, width=50, text=('U'))
    edit_colour_checkbox_u.grid(column=1, row=1, pady=(0, 8), sticky='ew')
    edit_colour_checkbox_b = ctk.CTkCheckBox(edit_colours_frame, width=50, text=('B'))
    edit_colour_checkbox_b.grid(column=2, row=1, pady=(0, 8), sticky='ew')
    edit_colour_checkbox_r = ctk.CTkCheckBox(edit_colours_frame, width=50, text=('R'))
    edit_colour_checkbox_r.grid(column=3, row=1, pady=(0, 8), sticky='ew')
    edit_colour_checkbox_g = ctk.CTkCheckBox(edit_colours_frame, width=45, text=('G'))
    edit_colour_checkbox_g.grid(column=4, row=1, padx=(0, 5), pady=(0, 8), sticky='ew')

    if 'W' in colours:
        edit_colour_checkbox_w.toggle()
    if 'U' in colours:
        edit_colour_checkbox_u.toggle()
    if 'B' in colours:
        edit_colour_checkbox_b.toggle()
    if 'R' in colours:
        edit_colour_checkbox_r.toggle()
    if 'G' in colours:
        edit_colour_checkbox_g.toggle()

    edit_rarity_frame = ctk.CTkFrame(edit_window)
    edit_rarity_frame.grid(row=6, column=0, padx=10, pady=5, sticky='ew', columnspan=2)
    edit_rarity_frame.grid_columnconfigure(0, weight=1)
    edit_rarity_label = ctk.CTkLabel(edit_rarity_frame, text='Rarity', font=('Helvetica', 12, 'bold'), text_color='white')
    edit_rarity_label.grid(column=0, row=0, padx=5, sticky='w')
    edit_rarity_entry = ctk.CTkComboBox(edit_rarity_frame, values=['Common','Uncommon','Rare','Mythic Rare'])
    edit_rarity_entry.set(rarity)
    edit_rarity_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')

    edit_count_frame = ctk.CTkFrame(edit_window)
    edit_count_frame.grid(row=7, column=0, padx=10, pady=5, sticky='ew', columnspan=2)
    edit_count_frame.grid_columnconfigure(0, weight=1)
    edit_count_label = ctk.CTkLabel(edit_count_frame, text='Quantity (Enter an Integer)', font=('Helvetica', 12, 'bold'), text_color='white')
    edit_count_label.grid(column=0, row=0, padx=5, sticky='w')
    edit_count_entry = ctk.CTkEntry(edit_count_frame)
    edit_count_entry.insert(0, count)
    edit_count_entry.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')

    edit_image_frame = ctk.CTkFrame(edit_window)
    edit_image_frame.grid(row=8, column=0, padx=10, pady=5, sticky='ew', columnspan=2)
    edit_image_frame.grid_columnconfigure(0, weight=1)
    edit_image_label = ctk.CTkLabel(edit_image_frame, text=img_path, font=('Helvetica', 12, 'bold'), text_color='white')
    edit_image_label.grid(column=0, row=0, padx=5, sticky='w')
    edit_image_button = ctk.CTkButton(edit_image_frame, text='Select a File', command=lambda: edit_image_label.configure(text=image_selection()))
    edit_image_button.grid(column=0, row=1, padx=5, pady=(0,5), sticky='ew')


    confirm_edit_button = ctk.CTkButton(edit_window, text='Edit', command=lambda: [init_edit(id, edit_name_entry, edit_cost_entry, edit_cmc_entry, edit_type_entry,
                                                                                        edit_subtype_entry, edit_colour_checkbox_w, edit_colour_checkbox_u,
                                                                                        edit_colour_checkbox_b, edit_colour_checkbox_r, edit_colour_checkbox_g,
                                                                                        edit_rarity_entry, edit_count_entry, edit_image_label),
                                                                                        edit_window.destroy(),
                                                                                        init_search()])
    confirm_edit_button.grid(row=9, column=1, padx=(5, 10), pady=(5,10), sticky='nesw')

    delete_card_button = ctk.CTkButton(edit_window, text='Delete Card', fg_color='#cf0000', hover_color='#750000', command=lambda: [db.delete_card(id), edit_window.destroy(), init_search()])
    delete_card_button.grid(row=9, column=0, padx=(10, 5), pady=(5,10), sticky='nesw')

    edit_window.grid_rowconfigure(9, weight=1)

def init_edit(id, edit_name_entry, edit_cost_entry, edit_cmc_entry, edit_type_entry,
            edit_subtype_entry, edit_colour_checkbox_w, edit_colour_checkbox_u,
            edit_colour_checkbox_b, edit_colour_checkbox_r, edit_colour_checkbox_g,
            edit_rarity_entry, edit_count_entry, edit_image_label):
    edit_data = {
        'name' : edit_name_entry.get(),
        'cost' : edit_cost_entry.get(),
        'cmc' : edit_cmc_entry.get(),
        'card_type' : edit_type_entry.get(),
        'subtype' : edit_subtype_entry.get(),
        'colour' : [
            'W' if edit_colour_checkbox_w.get() else '',
            'U' if edit_colour_checkbox_u.get() else '',
            'B' if edit_colour_checkbox_b.get() else '',
            'R' if edit_colour_checkbox_r.get() else '',
            'G' if edit_colour_checkbox_g.get() else ''
        ],
        'rarity' : edit_rarity_entry.get(),
        'count' : edit_count_entry.get(),
        'img_path' : edit_image_label.cget('text')
    }

    #remove empty strings from colour information 
    edit_data['colour'] = [color for color in edit_data['colour'] if color]
    edit_data['colour'] = ''.join(edit_data['colour'])
    edit_data['img_path'] = None if edit_data == 'Image' else edit_data['img_path']

    #merge colour values into a string
    edit_data = {key: (value if value !='' else None) for key, value in edit_data.items()}
    db.edit_query_constructor(id, **edit_data)

def image_selection():
    img_path = filedialog.askopenfilename(title='select a file: ', filetypes=[("Images", ("*.png", "*.jpg", "*.jpeg"))])
    if img_path:
        print(f"Selected file: {img_path}")
        return img_path

# set grid weights for dynamic resizing
app.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
app.grid_rowconfigure(5, weight=1)

app.mainloop()