#!/usr/bin/python

"""
TODO
"""

# import urllib
# from lxml import html
# import html5lib

import requests
import re
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, db

from models.film_model import FilmModel

URLS = {
    'valladolid': 'https://www.ocinerioshopping.es/'
}


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

    return upload_films_to_firebase([get_film_properties(film) for film in film_list])


def get_film_properties(film):
    """
    TODO
    """
    # ID
    id = int(film.find('h2').find('a').attrs['name'])

    # Title
    title = film.find('h2').text.strip()

    # Description
    description_container = film.find('div', id='descripcio')
    read_more_tag = description_container.find('a', class_='sprocket-readmore').text
    description = description_container.text.replace(read_more_tag, '').strip()
    full_descripton = description + film.find('span', id=re.compile(r'readmore.*')).text.strip()
    full_descripton = " ".join(full_descripton.strip().split(" "))

    return FilmModel(id, title, full_descripton)


def upload_films_to_firebase(films):
    """
    TODO
    """
    cred = credentials.Certificate('config/fire_base_config.json')

    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ocine-ca275.firebaseio.com/'
    })

    for film in films:
        ref = db.reference('films/' + str(film.id))
        ref.set({
            'title': film.title,
            'description': film.description
        })



def main():
    """
    TODO
    """

    get_web_contents()


if __name__ == '__main__':
    main()
