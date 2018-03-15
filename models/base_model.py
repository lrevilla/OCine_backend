"""
TODO
"""


class BaseModel(object):

    def to_json(self):
        """
        TODO
        """
        return {key: value for key, value in self.__dict__.iteritems()
                if not key.startswith('_')}
