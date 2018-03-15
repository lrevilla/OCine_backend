"""
TODO
"""


import re
import locale
from imdb import IMDb
from datetime import datetime
from base_model import BaseModel
from session_model import SessionModel


class FilmModel(BaseModel):
    """
    TODO
    """

    _imdb_instance = IMDb()

    def __init__(self, movie, film_html):
        locale.setlocale(locale.LC_TIME, "es_ES")
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
        session_list = self._film_html.find('div', class_='contingut').find_all("tr", class_="horari")
        sessions_by_day = {
            session.find("th").text: [hour.find("a").text.strip() for hour in session.find_all("td")]
            for session in session_list
        }

        datetime_sessions = [self.__sessions_to_datetime(week_day, day_sessions)
                             for week_day, day_sessions in sessions_by_day.items()]

        return [SessionModel(session.isoformat()).to_json() for session_sublist in datetime_sessions
                for session in session_sublist]

    def __sessions_to_datetime(self, day, sessions):
        """
        TODO
        """
        day = '-'.join([day.split(" ")[0], str(datetime.now().year)])
        return [datetime.strptime((" ".join([day, session])), '%d-%m-%Y %H:%M') for session in sessions]
