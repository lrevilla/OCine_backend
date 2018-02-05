"""
TODO
"""


import re

class FilmModel(object):
    """
    TODO
    """

    def __init__(self, id, title, description):
        self.id = id
        self.title = self.__format_text(title)
        self.description = self.__format_text(description)

    def __format_text(self, text):
        """
        TODO
        """

        return re.sub(r"\t", '', text)
