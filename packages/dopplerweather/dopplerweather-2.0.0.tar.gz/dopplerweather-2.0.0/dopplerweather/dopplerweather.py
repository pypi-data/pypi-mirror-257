import requests


class Weather:
    """
    Creates a Weather object, getting an apikey as an input and either a city name or
    both a latitude and a longitude.

    Package usage example:
    # Create a weather object using a city name:
    # The api key below is not guaranteed to work.
    # Get your own apikey from https://openweathermap.org/
    # And wait a couple of hours for the apikey to be activated.

    # Using city name
    >>> weather1 = Weather(apikey = "4b0286c52ef756c37eb4cc5a9a28e842", city = "Pune")

    # Using latitude and longitude co-ordinates
    >>> weather2 = Weather(apikey = "4b0286c52ef756c37eb4cc5a9a28e842", lat = 41.0, lon = -4.1)

    # Get complete weather data for the next 12 hours:
    >>> weather1.next_12h()

    # Get simplified weather data for the next 12 hours:
    >>> weather1.next_12h_simplified()

    Sample url to get sky condition icons:
    https://openweathermap.org/img/wn/10d@2x.png

    """
    def __init__(self, apikey, city=None, lat=None, lon=None):
        """
        Initializes the Weather class object.
        :param apikey: openweathermap apikey of user.
        :param city: city
        :param lat: latitude
        :param lon: longitude
        """
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?" \
                  f"q={city}&appid={apikey}&units=imperial"
        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?" \
                  f"lat={lat}&lon={lon}&appid={apikey}&units=imperial"
        else:
            raise TypeError("Provide either a city or lat and lon arguments.")
        if url:
            response = requests.get(url)
            self.data = response.json()
        if self.data['cod'] != '200':
            raise ValueError(self.data, self.data['message'])

    def next_12h(self):
        """
        Returns every 3-hour weather data for the next 12 hours.
        :return: dictionary
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """
        Returns date, temperature, and sky condition every 3 hours
        for the next 12 hours.
        :return: tuple of tuples
        """
        weather_data = []
        for dictionary in self.data['list'][:4]:
            weather_data.append([dictionary['dt_txt'],
                                 dictionary['main']['temp'],
                                 dictionary['weather'][0]['description'],
                                 dictionary['weather'][0]['icon']])
        return weather_data

