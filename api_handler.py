import requests
import copy

def search_card(cardname): #this method fetches card details from the scryfall database based on the cards exact name
    base_url = "https://api.scryfall.com/cards/named"
    params = {"exact" : cardname}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        card_data = response.json()

        print(f"Card Name: {card_data['name']}")
        print(f"CMC: {card_data['cmc']}")
        print(f"Cost: {card_data['mana_cost']}")
        print(f"Type: {card_data['type_line']}")
        print(f"Colour: {card_data['colors']}")
        print(f"Rarity: {card_data['rarity']}")

        output = {
            'name' : card_data['name'],
            'cmc' : card_data['cmc'],
            'cost' : card_data['mana_cost'],
            'type_line' : card_data['type_line'],
            'colors' : card_data['colors'],
            'rarity' : card_data['rarity'],
        }

        print(clean_data(output))

    except requests.exceptions.RequestException as e:
        print(f'An error occured: {e}')
    except KeyError as e:
        print(f'Unexpected data structure: Missing key {e}')

def clean_data(raw):
    cleaned = raw.copy()

    for key, value in list(cleaned.items()):
        if key == 'cmc':
            cleaned['cmc'] = int(value)

        elif key == 'cost':
            cleaned['cost'] = cleaned['cost'].replace("{",'').replace("}",'')

        elif key == 'colors':
            cleaned['colors'] = ''.join(value)

        elif key == 'type_line':
            parts = value.split('—')
            card_type = parts[0].strip()
            subtype = parts[1].strip() if len(parts) > 1 else None
            cleaned['card_type'] = card_type
            cleaned['subtype'] = subtype

        elif key == 'rarity':
            match cleaned['rarity']:
                case 'common':
                    cleaned['rarity'] = 'Common'
                case 'uncommon':
                    cleaned['rarity'] = 'Uncommon'
                case 'rare':
                    cleaned['rarity'] = 'Rare'
                case 'mythic':
                    cleaned['rarity'] = 'Mythic Rare'
        
        else:
            cleaned[key] = value

    del cleaned['type_line']
    
    return cleaned

def match_name(query): #this method returns matching names to the input parameter
    base_url = "https://api.scryfall.com/cards/search"
    name_query = f'name:{query}'
    params = {'q': name_query}

    try: 
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'data' in data:
            card_names = []
            print(f"Found {len(data['data'])} cards with names matching '{name_query}'")
            for i, card in enumerate(data['data']):
                print(f"{i+1}. - {card['name']}")
                card_names.append(card['name'])

            selected = int(input("Select Card Number: "))
            search_card(card_names[selected-1])
        
        else:
            print("No cards found.")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occured: {e}")

match_name(input("Search Cardname: "))