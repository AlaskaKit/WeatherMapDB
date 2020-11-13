import sys
from typing import Iterable
import requests
import psycopg2
from config import *


class WeatherFetcher:
    """
    Connector to API.
    """
    def __init__(self, ids: Iterable[int]):
        """
        A constructor for WeatherFetcher. Takes a list of the city IDs to request the API.
        URL, credentials and unites of measure are defined in the config file.
        :param ids: a list with city IDs.
        """
        self.url = API_URL
        self.units = UNITS
        self.appid = APPID
        self.city_id_list = ids
        
    def fetch_api(self) -> list:
        """
        Method to fetch data from api for the cities by their id.
        :return: List of dictionaries with complete data for each city.
        """
        
        def connect_to_api(url, parameters) -> dict:
            """
            Built-in function to actually connect to API.
            :param url: url to request
            :param parameters: dictionary with the parameters of the request.
            :return: in case of success returns weather data for requested cities as a list of dictionaries.
            """
            try:
                response = requests.get(url, timeout=2, params=parameters)
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                raise
            except requests.exceptions.RequestException:
                raise
                
            data: dict = response.json()
            
            if not data:
                raise ValueError(f"No data received from server for city id: {parameters['id']}!")
            
            return data

        result: list = []
        pars: dict = {'id': self.city_id_list[0], 'appid': self.appid, 'units': self.units}
       
        for city_id in self.city_id_list:
            pars["id"] = city_id
            try:
                chunk = connect_to_api(self.url, pars)
                result.append(chunk)
            except Exception as err:
                print(err, file=sys.stderr)
            
        print("Seems collecting data from API worked just fine.")
        
        return result

    
class WeatherSaver:
    """
    Checks received data and writes it to the database.
    """
    def __init__(self, cities: list):
        """
        Constructor takes weather data received and checks if there are necessary values for each city.
        :param cities: a list of dicts for each city.
        """
        
        self.values = []
        
        for city in cities:
            try:
                city_value = (city["id"], city["name"], city["weather"][0]["description"],
                              city["main"]["temp"], city["main"]["pressure"], city["main"]["humidity"],
                              city["visibility"], city["wind"]["speed"], city["wind"]["deg"], city["clouds"]["all"])
                self.values.append(city_value)
                
            except KeyError as data_error:
                print(f"Invalid data received. Chunk index: {cities.index(city)}", data_error, file=sys.stderr)
                sys.exit(1)
                
    def write_to_db(self):
        """
        Writes prepared data to DB using psycopg2 library.
        DB credentials and parameters are set in the config file.
        If requested city already present in the table, its values are being updated.
        Throws error if DB is not found and if there are no required table in the DB.
        :return: the writing/updating status if there were no errors.
        """
        # connect to db
        try:
            conn = psycopg2.connect(
                host=HOST,
                database=DBNAME,
                user=USER,
                password=PASSWORD
            )
        except psycopg2.Error as err:
            print(err.pgerror, file=sys.stderr)
            sys.exit(1)
        
        # creating cursor
        cursor = conn.cursor()
        
        # creating table in case it doesn't exits
        try:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS public.{UNSORTED_W} "
                           f"("
                           f"city_id integer NOT NULL, "
                           f"city_name character varying(100) NOT NULL, "
                           f"weather_description character varying(50) NOT NULL, "
                           f"temperature real NOT NULL, "
                           f"pressure integer NOT NULL, "
                           f"humidity integer NOT NULL, "
                           f"visibility integer NOT NULL, "
                           f"wind_speed real NOT NULL, "
                           f"wind_dir integer NOT NULL, "
                           f"clouds_all integer NOT NULL, "
                           f"CONSTRAINT {UNSORTED_W}_pkey PRIMARY KEY (city_id)"
                           f") TABLESPACE {TABLESPACE}")
                      
        except psycopg2.Error as err:
            print(err.pgerror, file=sys.stderr)
            sys.exit(1)
        
        # inserting/updating values
        for city_data in self.values:
            try:
                cursor.execute("INSERT INTO unsorted_weather (city_id, city_name, weather_description, temperature, "
                               "pressure, humidity, visibility, wind_speed, wind_dir, clouds_all) VALUES "
                               "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                               "ON CONFLICT (city_id) DO UPDATE "
                               "SET city_id = excluded.city_id, "
                               "city_name = excluded.city_name, "
                               "weather_description = excluded.weather_description, "
                               "temperature = excluded.temperature, "
                               "pressure = excluded.pressure, "
                               "humidity = excluded.humidity, "
                               "visibility = excluded.visibility, "
                               "wind_speed = excluded.wind_speed, "
                               "wind_dir = excluded.wind_dir, "
                               "clouds_all = excluded.clouds_all",
                               city_data)
            except psycopg2.Error as err:
                print(err.pgerror, file=sys.stderr)
                sys.exit(1)
        
        # commit transaction
        conn.commit()
        
        # close cursor
        cursor.close()
        
        # close connection
        conn.close()
        
        print(f"Transaction executed, {len(self.values)} rows have been written and/or updated.")
        
    def __str__(self):
        """
        String method for debugging purposes.
        :return: Data processed and prepared for writing to the DB.
        """
        return str(self.values)
        

if __name__ == '__main__':
    fetcher = WeatherFetcher(CITIES)
    cts = fetcher.fetch_api()
    db_writer = WeatherSaver(cts)
    db_writer.write_to_db()
