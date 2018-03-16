"""
TODO
"""


import re
import locale
from imdb import IMDb
from base_model import BaseModel
from session_model import SessionModel


class FilmModel(BaseModel):
    """
    TODO
    """

    _imdb_instance = IMDb()

    def __init__(self, movie, ocine_id, film_html):
        locale.setlocale(locale.LC_TIME, "es_ES")
        self.ocine_id = ocine_id
        self._movie = movie
        self._film_html = film_html
        self._imdb_id = int(self._movie.imdb.replace('tt', ''))
        self._imdb_movie = self._imdb_instance.get_movie(self._imdb_id)

        self.__populate_fields()

    def __populate_fields(self):
        """
        TODO
        """

        self._id = self._movie.id
        self.title = self._movie.title
        self.description = self._movie.overview
        self.duration = self.__get_movie_duration_string()
        self.release_date = self._movie.releasedate.strftime('%d %B %Y')
        self.rating = self._movie.userrating * 10
        self.genres = [genre.name for genre in self._movie.genres]
        self.casting = [{'name': cast.name, 'character': cast.character} for cast in self._movie.cast]
        self.director = [crew.name for crew in self._movie.crew if crew.job == 'Director'][0]
        self.cover_url = self.__get_cover_url()
        self.trailer_urls = [trailer.geturl() for trailer in self._movie.youtube_trailers]
        self.sessions = self.__get_sessions()

    def __get_movie_duration_string(self):
        """
        TODO
        """
        self.runtime = self._movie.runtime

        if not self.runtime:
            if 'runtimes' not in self._imdb_movie or not self._imdb_movie['runtimes']:
                self.runtime = int(self._film_html.find('div', class_='type').text.split(":")[1].split(".")[0].strip())
            else:
                self.runtime = int(self._imdb_movie['runtimes'][0])

        return str(self.runtime / 60) + ' h ' + str(self.runtime % 60) + ' min'

    def __get_cover_url(self):
        """
        TODO
        """
        url_fragments = self._imdb_movie['cover url'].split('@')
        return '@'.join([url_fragments[0], '._SY720_.jpg'])

    def __get_sessions(self):
        """
        TODO
        """
        session_list = self._film_html.find('div', class_='contingut').find_all('tr', class_='horari')
        return [SessionModel(day_session_html.find('th').text.split(' ')[0], session).to_json()
                for day_session_html in session_list
                for session in day_session_html.find_all('a', id=re.compile('^Tips-'))]
