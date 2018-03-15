"""
TODO
"""

import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

from base_model import BaseModel
from seat_model import SeatModel
from utils.constants import SeatTypes


class SessionModel(BaseModel):

    def __init__(self, date_string, session_html):
        self.time = self.__get_iso_time(date_string, session_html)
        self._params = self.__get_params(session_html)
        if self._params:
            self.seats_grid = self.__get_seats_grid()

    def __get_iso_time(self, date_string, session_html):
        """
        TODO
        """
        full_date_string = '-'.join([date_string, str(datetime.now().year)])
        session_string = session_html.text.strip()

        return datetime.strptime(' '.join([full_date_string, session_string]), '%d-%m-%Y %H:%M').isoformat()

    def __get_params(self, session_html):
        """
        TODO
        """
        if 'onclick' not in session_html.attrs:
            return None

        parameters = [param for param in session_html.attrs['onclick'].split(';') if '=' in param]
        return {parameter.split('=')[0].split('.')[2]: parameter.split('=')[1].replace("'", '')
                for parameter in parameters}

    def __get_seats_grid(self):
        """
        TODO
        """
        room_html = BeautifulSoup(requests.post(self._params['action'], data=self._params).text, 'html.parser')
        seats_grid = room_html.find('div', class_='bloc').find_all('table')[1].find_all('tr')

        # seat_list = [SeatModel(seats_grid[row].find_all('td')[cell].find('input'), row, cell)
        #              for row in range(0, len(seats_grid))
        #              for cell in range(0, len(seats_grid[row].find_all('td')))]
        seat_list = []

        for row in range(0, len(seats_grid)):
            for cell in range(0, len(seats_grid[row].find_all('td'))):
                current_seat = SeatModel(seats_grid[row].find_all('td')[cell].find('input'), row, cell)
                if current_seat.type != SeatTypes.DISABLED:
                    print('adding seat ' + str(current_seat.row) + ", " + str(current_seat.column))
                    seat_list.append(current_seat.to_json())

        # return [seat for seat in seat_list if seat.type != SeatTypes.DISABLED]
        return seat_list
