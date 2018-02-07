"""
TODO
"""


import re
import locale


class FilmModel(object):
    """
    TODO
    """

    def __init__(self, movie):
        locale.setlocale(locale.LC_TIME, "es_ES")
        self._movie = movie
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
        self.poster_urls = {self.__get_size_name(size): poster.geturl(size) for poster in self._movie.posters
                            for size in poster.sizes()}

    def __get_size_name(self, size):
        """
        TODO
        """
        if size.startswith('w'):
            return size.replace('w', '')

        return size

    def __get_movie_duration_string(self):
        """
        TODO
        """
        return str(self._movie.runtime / 60) + ' h ' + str(self._movie.runtime % 60) + ' min'

    def to_json(self):
        """
        TODO
        """

        return {key: value for key, value in self.__dict__.iteritems() if not key.startswith('_')}
