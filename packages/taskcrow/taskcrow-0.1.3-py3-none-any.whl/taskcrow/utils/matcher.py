from difflib import SequenceMatcher

from naverplaceapi import Client

from module.utils.coordinate import haversine_distance


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def match_restaurant(restaurant_name, road_address, searched_results):
    candiate_store = find_similar_store_by_name(restaurant_name, searched_results)
    nearest_store = find_similar_address_store(road_address, searched_results)

    if nearest_store is not None:
        return candiate_store
    elif candiate_store is not None:
        return nearest_store

    return None


def find_similar_store_by_name(keyword, stores):
    most_similarity = 0
    most_similarity_idx = 0
    for i, store in enumerate(stores):
        # naverplace_rest_name = store['title']
        naverplace_rest_name = store['name']
        similarity = similar(keyword, naverplace_rest_name)

        if similarity > most_similarity:
            most_similarity = similarity
            most_similarity_idx = i

    if most_similarity < 0.6:
        return None

    return stores[most_similarity_idx]


def find_similar_address_store(address, stores):
    api = Client()
    response = api.geocode(address)
    addresses = response['addresses']
    if len(addresses) == 0:
        return None
    lon = addresses[0]['x']
    lat = addresses[0]['y']

    nearest_distance = 9999
    nearest_idx = -1

    for i, store in enumerate(stores):
        target_road_address = store['roadAddress']
        if target_road_address == '':
            target_road_address = store['address']
        target_response = api.geocode(target_road_address)
        try:
            target_addresses = target_response['addresses']
        except Exception as e:
            print("e", e)
            continue
        if len(target_addresses) == 0:
            continue
        target_lon = target_addresses[0]['x']
        target_lat = target_addresses[0]['y']
        distance = haversine_distance(float(lat), float(lon), float(target_lat), float(target_lon))
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_idx = i

    if nearest_distance > 0.4:
        return None

    return stores[nearest_idx]
