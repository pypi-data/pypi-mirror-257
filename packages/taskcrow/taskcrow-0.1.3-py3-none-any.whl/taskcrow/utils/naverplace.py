
def extract_restaurant_fields_in_fragments(fragments):
    restaurant_key_names = ['restaurant', 'place']
    restaurants = []
    for fieldname in fragments.keys():
        is_restaurant_info = False
        for restaurant_key_name in restaurant_key_names:
            if restaurant_key_name.lower() in fieldname.lower():
                is_restaurant_info = True
                break
        if not is_restaurant_info:
            continue
        restaurants.append(fragments[fieldname])
    return restaurants
