import requests
from database import api_image_file

def search_card(cardname): #this method fetches card details from the scryfall database based on the cards exact name
    base_url = "https://api.scryfall.com/cards/named"
    params = {"exact" : cardname}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        card_data = response.json()

        output = {
            'name' : card_data['name'],
            'cmc' : card_data['cmc'],
            'cost' : card_data['mana_cost'],
            'type_line' : card_data['type_line'],
            'colors' : card_data['colors'],
            'rarity' : card_data['rarity'],
        }

        image_url = card_data.get('image_uris', {}).get('normal', None)
        if not image_url:
            if 'card_faces' in card_data:
                image_url = card_data['card_faces'][0].get('image_uris', {}).get('Normal', None)
            else:
                image_url = None
        
        img_path = save_image(image_url, cardname)
        output['img_path'] = img_path

        print(clean_data(output))
        return clean_data(output)

    except requests.exceptions.RequestException as e:
        print(f'An error occured: {e}')
    except KeyError as e:
        print(f'Unexpected data structure: Missing key {e}')

def save_image(image_url, cardname):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        img_path = api_image_file(response.content, cardname)
        return img_path

    except requests.exceptions.RequestException as e:
        print(f'Failed to download image {e}')

def clean_data(original_dict):
    cleaned = original_dict.copy()

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
    base_url = "https://api.scryfall.com/cards/autocomplete"
    params = {'q': query}

    if query:
        try: 
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'data' in data:
                card_names = data['data']
                print(f"Found {len(data['data'])} cards with names matching '{query}'")
                print(card_names)
                return card_names
            
            else:
                print("No cards found.")
                return []

        except requests.exceptions.RequestException as e:
            print(f"An error occured: {e}")