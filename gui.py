import customtkinter as ctk
import database as db
import logic

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Database Manager")
app.geometry("1000x400")

#search bar and add button
title = ctk.CTkLabel(app, text='Your Cards', font=('Helvetica', 36, 'bold'), text_color='white')
title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky='w')

add_button = ctk.CTkButton(app, text='+', command=lambda: add_card_window())
add_button.grid(row=0, column=5, padx=(5, 20), pady=(20, 0), sticky='ew')

namesearch = ctk.CTkEntry(app, placeholder_text='Search by Card Name')
namesearch.grid(row=1, column=0, columnspan=5, padx=(20, 5), pady=10, sticky='ew')

searchbutton = ctk.CTkButton(app, text='Search', command=lambda: perform_search()) #lambda is used to pass parameters to a function
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
sort_by_dropdown = ctk.CTkOptionMenu(sort_by_frame, values=['Date Added (New - Old)', 'Date Added (Old - New)', 'Alphabetical (A-Z)', 'Aplhabetical (Z-A)'])
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
grid_scroll = ctk.CTkScrollableFrame(grid, fg_color='red')
grid_scroll.grid(row=0, column=0, sticky='nesw')
grid_scroll.grid_columnconfigure((0, 1, 2, 3), weight=1)

def add_card_window():
    window = ctk.CTkToplevel()
    window.geometry('300x200')
    window.title('Add a card')

#take name and filter settings from search bar and call display with search results
def perform_search():
    name = namesearch.get()
    cmc = cmc_filter.get()
    cost = cost_filter.get()
    type = type_filter.get()
    subtype = subtype_filter.get()
    is_white = colour_checkbox_w.get()
    is_blue = colour_checkbox_u.get()
    is_black = colour_checkbox_b.get()
    is_red = colour_checkbox_r.get()
    is_green = colour_checkbox_g.get()
    rarity = rarity_filter.get()
    results = logic.card_search(name, cmc, cost, type, subtype, is_white, is_blue, is_black, is_red, is_green, rarity)
    print(f'Results {results}')
    display_results(results)
    

def clear_results():
    for widget in list_scroll.winfo_children():
        widget.destroy()
    for widget in grid_scroll.winfo_children():
        widget.destroy()

#card display frames inside scrollable window
def display_results(results): #results is a list of tuples passed by the card search function
    clear_results()
    for i, row in enumerate(results):
        
        id, name, cmc, cost, type, subtype, colour, rarity, count = [
                    "N/A" if value is None else value for value in row
                ]

        list_card_frame = ctk.CTkFrame(list_scroll)
        list_card_frame.grid(row=i, column=0, pady=2.5, sticky='new')
        list_card_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)  # Distribute column weight

        # Name Frame (list)
        name_frame_display = ctk.CTkFrame(list_card_frame)
        name_frame_display.grid(row=0, column=0, padx=(5, 2.5), pady=5, sticky='ew')  # remove padding around frame
        name_frame_display.grid_columnconfigure(0, weight=1)  
        name_label = ctk.CTkLabel(name_frame_display, text=name, font=('Helvetica', 14, 'bold'))
        name_label.grid(row=0, column=0, padx=5, pady=0, sticky='ew')  # Ensure no padding for the label

        # Cost Frame (list)
        cmc_frame_display = ctk.CTkFrame(list_card_frame)
        cmc_frame_display.grid(row=0, column=1, padx=2.5, pady=5, sticky='ew')
        cmc_frame_display.grid_columnconfigure(0, weight=1)
        cmc_label = ctk.CTkLabel(cmc_frame_display, text=f'CMC: {cmc}', font=('Helvetica', 14, 'bold'))
        cmc_label.grid(row=0, column=0, padx=5, pady=0, sticky='ew')

        # Converted Mana Cost (CMC) Frame (list)
        cost_frame_display = ctk.CTkFrame(list_card_frame)
        cost_frame_display.grid(row=0, column=2, padx=2.5, pady=5, sticky='ew')
        cost_frame_display.grid_columnconfigure(0, weight=1)  
        cost_label = ctk.CTkLabel(cost_frame_display, text=f'Cost: {cost}', font=('Helvetica', 14, 'bold'))
        cost_label.grid(row=0, column=0, padx=5, pady=0, sticky='ew')

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
        edit_button = ctk.CTkButton(list_card_frame, text='Edit', width=40)
        edit_button.grid(row=0, column=8, padx=(0, 5), pady=5, sticky='e')

        #grid view card frame
        grid_card_frame = ctk.CTkFrame(grid_scroll)
        grid_card_frame.grid(row=i // 4, column=i % 4, pady=5, padx=5, sticky='ew')
            

# set grid weights for dynamic resizing
app.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
app.grid_rowconfigure(5, weight=1)

app.mainloop()