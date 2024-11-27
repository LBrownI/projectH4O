import requests
import os
import json
from pprint import pprint

with open('API_KEY.key', 'r') as file:
    API_KEY = file.read().strip()

PROJECT = "all";
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

def test_checkPlant():

    uploads_dir = "backend/uploads"
    latest_image = max([os.path.join(uploads_dir, f) for f in os.listdir(uploads_dir)], key=os.path.getctime)
    # image_path_1 = "backend/uploads/test1.jpg"
    image_path_1 = latest_image
    image_data_1 = open(image_path_1, 'rb')

    image_path_2 = "./image_2.jpeg"
    image_data_2 = open(image_path_2, 'rb')

    data = { 'organs': ['flower', 'leaf'] }

    files = [
    ('images', (image_path_1, image_data_1)),
    ('images', (image_path_2, image_data_2))
    ]

    req = requests.Request('POST', url=api_endpoint, files=files, data=data)
    prepared = req.prepare()

    s = requests.Session()
    response = s.send(prepared)
    json_result = json.loads(response.text)

    pprint(response.status_code)
    pprint(json_result)
        # Extract useful data from the first result
    first_result = json_result['results'][0]

    # Species details
    species_info = first_result['species']
    common_names = species_info['commonNames']
    scientific_name = species_info['scientificName']
    scientific_name_authorship = species_info['scientificNameAuthorship']
    family = species_info['family']['scientificName']
    genus = species_info['genus']['scientificName']

    # Related identifiers
    gbif_id = first_result['gbif']['id']
    powo_id = first_result['powo']['id']
    score = first_result['score']

    # Gather all useful data
    useful_data = {
        'common_names': common_names,
        'scientific_name': scientific_name,
        'scientific_name_authorship': scientific_name_authorship,
        'family': family,
        'genus': genus,
        'gbif_id': gbif_id,
        'powo_id': powo_id,
        'score': score
    }

    # Print all useful data
    print(useful_data)
    return useful_data
    
# test_checkPlant()