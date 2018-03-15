"""
TODO
"""

from base_model import BaseModel
from utils.constants import SeatTypes, SeatStatus


class SeatModel(BaseModel):

    def __init__(self, seat_html, row, column):
        self._seat_html = seat_html
        self.type = self.__get_type()
        self.available = self.__is_available()
        self.row = row
        self.column = column

    def __get_type(self):
        """
        TODO
        """
        if 'botonnormal' in self._seat_html.attrs['class'] or 'botonnormalocupat' in self._seat_html.attrs['class']:
            return SeatTypes.REGULAR
        elif 'botonminus' in self._seat_html.attrs['class']:
            return SeatTypes.MINUSVALID
        elif 'botonfidelitat' in self._seat_html.attrs['class']:
            return SeatTypes.VIP
        else:
            return SeatTypes.DISABLED

    def __is_available(self):
        """
        TODO
        """

        return 'disabled' in self._seat_html.attrs.keys()
