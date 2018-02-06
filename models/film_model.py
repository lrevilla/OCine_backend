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
        self.duration = self._movie.runtime
        self.release_date = self._movie.releasedate.strftime('%d %B %Y')
        self.genres = [genre.name for genre in self._movie.genres]
        self.casting = [{'name': cast.name, 'character': cast.character} for cast in self._movie.cast]
        self.director = [crew.name for crew in self._movie.crew if crew.job == 'Director'][0]

        get_size_name = lambda size: size.replace('w', '') if size.startswith('w') else size
        self.poster_urls = {get_size_name(size): poster.geturl(size) for poster in self._movie.posters
                            for size in poster.sizes()}

    def to_json(self):
        """
        TODO
        """

        return {key: value for key, value in self.__dict__.iteritems() if not key.startswith('_') }
