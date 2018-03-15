#!/usr/bin/python

"""
TODO
"""

# import urllib
# from lxml import html
# import html5lib

import requests
import re
import json
import tmdb3
import firebase_admin

from collections import namedtuple
from bs4 import BeautifulSoup
from firebase_admin import credentials, db

from models.film_model import FilmModel

URLS = {
    'valladolid': 'https://www.ocinerioshopping.es/'
}


def load_configuration_file():
    """
    TODO
    """
    global config
    config_dict = json.load(open('config/config.json'))
    config = namedtuple('config', config_dict.keys())(*config_dict.values())


def get_web_contents():
    """
    TODO
    """

    for url in URLS:
        current_url = URLS[url]
        html_page = requests.get(current_url)
        html_page = BeautifulSoup(html_page.text, 'html.parser')
        get_films_in_page(html_page)


def get_films_in_page(page):
    """
    TODO
    """
    film_list = page.find('div', class_='component-content').find_all('div', class_='rt-block component-block')

    return upload_films_to_firebase([get_film_properties(film) for film in film_list if film is not None])


def get_film_properties(html_film_node):
    """
    TODO
    """
    # Title
    title = html_film_node.find('h2').text.strip()
    ocine_id = int(html_film_node.find('h2').find('a').attrs['name'])

    search_results = tmdb3.searchMovie(title)
    if len(search_results):
        return FilmModel(search_results[0], ocine_id, html_film_node)

    return None


def upload_films_to_firebase(films):
    """
    TODO
    """
    cred = credentials.Certificate('config/firebase_config.json')

    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ocine-ca275.firebaseio.com/'
    })

    for film in films:
        if film is not None:
            ref = db.reference('films/' + str(film._id))
            ref.set(film.to_json())


def main():
    """
    TODO
    """

    load_configuration_file()
    tmdb3.set_key(config.tmdb_api_key)
    tmdb3.set_locale('es', 'ES')
    get_web_contents()


if __name__ == '__main__':
    main()
