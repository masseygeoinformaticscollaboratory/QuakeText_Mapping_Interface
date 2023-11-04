import json
import string

import pandas as pd
import xmltodict
import xml.etree.ElementTree as ET

check_locations = {}


def is_key_in_list_of_dicts(key, list_of_dicts):
    for dictionary in list_of_dicts:
        if key in dictionary:
            return True
    return False


def extract_values_for_key(key, list_of_dicts):
    values = 0
    for dictionary in list_of_dicts:
        if key in dictionary:
            values = dictionary[key]
    return values


def update_values_for_key(key, new_value, list_of_dicts):
    for dictionary in list_of_dicts:
        if key in dictionary:
            dictionary[key] = new_value


def gettext(text, loc_start, loc_end):
    before_loc = text[:loc_start]
    location = text[loc_start:loc_end]
    after_loc = text[loc_end + 1:] if loc_end < len(text) - 1 else ''

    before_tokens = before_loc.split()
    substring_token = [location]
    after_tokens = after_loc.split()

    tokens = before_tokens + substring_token + after_tokens
    occurrences = 0

    if text in check_locations:
        if is_key_in_list_of_dicts(location, check_locations[text]):
            occurrences = extract_values_for_key(location, check_locations[text])
            occurrences += 1
            update_values_for_key(location, occurrences, check_locations[text])
        else:
            check_locations[text].append({location: 1})
    else:
        check_locations[text] = [{location: 1}]

    location_index = tokens.index(location)
    if occurrences > 0:
        count = 0
        for i, token in enumerate(tokens):
            if location == token and count < occurrences:
                count += 1
                if count == occurrences:
                    location_index = i
                    break
            else:
                continue

    if location_index < 25:
        index_start = 0
    else:
        index_start = location_index - 25

    if (location_index + 25) >= len(tokens):
        index_end = len(tokens) - 1
    else:
        index_end = location_index + 25

    text = ' '.join(tokens[index_start:index_end])

    return text


def gettext2(text, loc_start, loc_end):
    before_loc = text[:loc_start]
    location = text[loc_start:loc_end]
    after_loc = text[loc_end + 1:] if loc_end < len(text) - 1 else ''

    before_tokens = before_loc.split()
    substring_token = [location]
    after_tokens = after_loc.split()

    tokens = before_tokens + substring_token + after_tokens

    if len(tokens) < 512:
        return text

    occurrences = 0
    if text in check_locations:
        if is_key_in_list_of_dicts(location, check_locations[text]):
            occurrences = extract_values_for_key(location, check_locations[text])
            occurrences += 1
            update_values_for_key(location, occurrences, check_locations[text])
        else:
            check_locations[text].append({location: 1})
    else:
        check_locations[text] = [{location: 1}]

    location_index = tokens.index(location)
    if occurrences > 0:
        count = 0
        for i, token in enumerate(tokens):
            if location == token and count < occurrences:
                count += 1
                if count == occurrences:
                    location_index = i
                    break
            else:
                continue

    if location_index < 255:
        index_start = 0
    else:
        index_start = location_index - 255

    if (location_index + 255) >= len(tokens):
        index_end = len(tokens) - 1
    else:
        index_end = location_index + 255

    text = ' '.join(tokens[index_start:index_end])

    return text


def main():
    tree = ET.parse('Original Data/lgl.xml')
    root = tree.getroot()
    xml_dict = xmltodict.parse(ET.tostring(root))
    articles = xml_dict['articles']['article']

    col_names = ['text', 'location', 'lat', 'lon', 'geonameID']
    data = pd.DataFrame(columns=col_names)

    for item in articles:
        toponyms = item['toponyms']['toponym']

        for toponym in toponyms:

            if 'gaztag' in toponym:
                if 'start' in toponym:
                    new_row_data = {
                        'text': gettext2(item['text'], int(toponym['start']), int(toponym['end'])),
                        'location': toponym['phrase'], 'lat': toponym['gaztag']['lat'],
                        'lon': toponym['gaztag']['lon'],
                        'geonameID': toponym['gaztag']['@geonameid']}

                    data.loc[len(data)] = new_row_data

    data.to_csv('LGLProcessed512.csv', index=False)


main()
