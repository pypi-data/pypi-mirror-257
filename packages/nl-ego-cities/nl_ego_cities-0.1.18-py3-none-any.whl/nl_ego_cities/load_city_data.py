import json
import pandas as pd
import numpy as np
from difflib import get_close_matches
from typing import Tuple
from .city_coords import city_json



def location_json(city='', street=''):
    lat, lon = [None, None]
    if city != '':
        if city in city_json.keys():
            lat, lon = city_json[city]['lat'], city_json[city]['lon']
        else:
            lat = 91
            lon = 181
    return lat, lon
def get_location(city):
    lat, lon = location_json(city=city)
    return lat, lon

#####################################
#   find similar string             #
#####################################
def find_most_similar_city(input_str):
    city_names = city_json.keys()
    closest_matches = get_close_matches(input_str, city_names, n=1)
    if closest_matches:
        return closest_matches[0]
    else:
        return ''


def get_lat_lon(df, city_column: str, find_similar: bool = False) -> Tuple[list, list]:
    """
    Get latitude and longitude of the city column's value.

    Args:
        df: DataFrame containing city column.
        city_column: Name of the column containing city names.
        find_similar: Whether to find similar city names if exact match is not found. Default is False.

    Returns:
        Tuple containing lists of latitude and longitude values.
    """
    if find_similar:
        df['similar_city'] = df[city_column].apply(lambda x: find_most_similar_city(x))
    else:
        df['similar_city'] = df[city_column]
    
    # Ensure 'similar_city' column is not empty
    if df['similar_city'].isnull().any():
        raise ValueError("Some city names could not be resolved.")
    
    latitudes, longitudes = zip(*df['similar_city'].apply(get_location))
    return list(latitudes), list(longitudes)
