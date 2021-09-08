import pycurl
import urllib.parse as urlparse
import pandas as pd
import certifi
import typing
import json
import numpy as np
import os
import pathlib
import warnings
import datetime

from io import BytesIO


class DataLoader:
    """
    Implements methods to fetch data from https://data.covid19india.org/ for 
    states/country, timeseries/daily as pandas DataFrame or a dictionary of 
    DataFrames.

    Once instantiated, it makes *one call* to the API server, and caches entire 
    timeseries data or entire daily data in the object itself. Once you've constructed the
    desired DataFrames, consider 'del <object>' to save on memory.

    Or you can get the dictionary of all DataFrames using the property 

    LIMITATIONS:
        1. 2021-07-16: Only gets the statewise data
    TODO: Get and process distric-wise data.

    Examples:
    >>> # Instantiate
    >>> dl = DataLoader()
    """
    def __init__(self) -> None:
        BASE_URL = 'https://data.covid19india.org/v4/min/'
        self.API_TYPE_URL = {
            'timeseries': urlparse.urljoin(BASE_URL, 'timeseries.min.json'),
            'daily': urlparse.urljoin(BASE_URL, 'data.min.json'),
        }

        # TODO: Move these objects to an external database / file.
        self.CODES = {
            "AP": "Andhra Pradesh", "AR": "Arunachal Pradesh", "AS": "Assam",
            "BR": "Bihar", "CT": "Chhattisgarh", "GA": "Goa", "GJ": "Gujarat",
            "HR": "Haryana", "HP": "Himachal Pradesh", "JH": "Jharkhand",
            "KA": "Karnataka", "KL": "Kerala", "MP": "Madhya Pradesh", 
            "MH": "Maharashtra", "MN": "Manipur", "ML": "Meghalaya", 
            "MZ": "Mizoram", "NL": "Nagaland", "OR": "Odisha", "PB": "Punjab",
            "RJ": "Rajasthan", "SK": "Sikkim", "TN": "Tamil Nadu",
            "TG": "Telangana", "TR": "Tripura", "UT": "Uttarakhand", 
            "UP": "Uttar Pradesh", "WB": "West Bengal", 
            "AN": "Andaman and Nicobar Islands", "CH": "Chandigarh", 
            "DN": "Dadra and Nagar Haveli and Daman and Diu", "DL": "Delhi",
            "JK": "Jammu and Kashmir", "LA": "Ladakh", "LD": "Lakshadweep",
            "PY": "Puducherry", "TT": "India"
        }

        self.STATES = {v.lower(): k for k, v in self.CODES.items()}

        self.__all_timeseries_data = None
        self.__daily_dfs = None
        # self.__all_daily_data = None
        current_file_path = os.path.abspath(__file__)
        path = pathlib.Path(current_file_path)
        
        self.data_dir = 'data'
        for p in path.parents:
            if str(p).endswith('covid_modeling'):
                self.data_dir = os.path.join(p, self.data_dir)
                break
        os.makedirs(self.data_dir, exist_ok=True)

    def search_state_code(self, state: str) -> typing.Dict[str, str]:
        """
        Get a list of state and codes matching partial of full state name.
        
        Example:
        >>> dl = DataLoader()

        >>> dl.get_state_code("Jammu")
        {'jammu and kashmir': 'JK'}

        >>> dl.get_state_code("and")
        {'andhra pradesh': 'AP', 'jharkhand': 'JH', 'nagaland': 'NL', 'uttarakhand': 'UT', 'andaman and nicobar islands': 'AN', 'chandigarh': 'CH', 'dadra and nagar haveli and daman and diu': 'DN', 'jammu and kashmir': 'JK'}
        """
        return {key: val 
                for key, val in self.STATES.items() 
                if state.lower() in key}

    def get_all_states_with_codes(self) -> typing.Dict[str, str]:
        return {key: val 
                for key, val in self.STATES.items()}
    
    def get_available_states(self) -> typing.List[str]:
        """
        Get the list of all available state segments.
        """
        return list(self.CODES.values())

    def get_data(
        self,
        state_codes: typing.Union[str, typing.List[str]]="TT",
        data_type: str ='timeseries'
    ) -> typing.Union[pd.DataFrame, typing.Dict[str, pd.DataFrame]]:
        """
        Get the data as a DataFrame or a dictionary of DataFrames

        Parameters:
        state_codes: Union[str, Lits(str)] -- Required state data for given state code 
                     as a string (one state) or as a list of string (multiple states)

                     if state_codes = 'all', entire data dict is returned. See the method
                     get_all_timeseries and get_all_daily for compact signature version

                     if state_codes is a non-empty list of strings, returns the data as dict '
                     whose keys are the corresponding state codes and the values are the
                     corresponding DataFrames.

                     if it is an empty list, an error is raised!

                     if the list contains some valid and some invalid codes, DataFrames for
                     only valid codes is returned (as a best effort)

                     you can find available states codes using the rather premitive search 
                     method: search_state_code
        data_type: str -- only two flavours are considered: 'timeseries' and 'daily'

        """
        if isinstance(state_codes, list):
            state_codes_get = [state_code for state_code in state_codes if state_code in self.CODES]
            if len(state_codes_get) == 0:
                raise ValueError(f'None of the states {state_codes} found.')
            diff = list(set(state_codes) - set(state_codes_get))
            if len(diff) > 0:
                warnings.warn(f'States {diff} not found. Getting data for {state_codes_get} only.')
            return self.__states(state_codes_get, data_type)
        
        if state_codes.lower() == 'all':
            return self.__all(data_type)
        
        if state_codes in self.CODES:
            return self.__state(state_codes, data_type)
        
        raise ValueError(f'State "{state_codes}" not found. Call the method "get_state_code" to check.')
    
    def __state(self, state_code: str, data_type: str) -> pd.DataFrame:
        return self.__all(data_type)[state_code]

    def __states(self, states: typing.List[str], data_type: str) -> typing.Dict[str, pd.DataFrame]:
        return {key: val for key, val in self.__all(data_type).items() if key in states}

    def __all(self, data_type: str) -> typing.Dict[str, pd.DataFrame]:
        if data_type not in self.API_TYPE_URL.keys():
            raise ValueError(f'Wrong data_type argument. Must be one of {self.API_TYPE_URL.keys()}')

        body = None
        
        self.current_data_file = os.path.join(self.data_dir, f"st-{datetime.datetime.now().date()}.json")
        if os.path.exists(self.current_data_file):
            warnings.warn("Data is up-to-date. Using local files.")
            f = open(self.current_data_file, 'r')
            body = json.load(f)
            f.close()
        else:
            body = self.__perform_curl(data_type)
            f = open(self.current_data_file, 'w')
            json.dump(body, f)
            f.close()

        if self.__all_timeseries_data is None:
            self.__all_timeseries_data = self.__process_timeseries_payload(body)

        if data_type == 'timeseries':
            return self.__all_timeseries_data
        
        if data_type == 'daily':
            if self.__daily_dfs is None:
                columns = self.__all_timeseries_data['TT'].columns
                df_today = pd.DataFrame(index=self.__all_timeseries_data.keys(), columns=columns)
                df_yesterday = pd.DataFrame(index=self.__all_timeseries_data.keys(), columns=columns)
                for key in self.__all_timeseries_data.keys():
                    df_today.loc[key] = self.__all_timeseries_data[key].iloc[-1]
                    df_yesterday.loc[key] = self.__all_timeseries_data[key].iloc[-2]
                self.__daily_dfs = [df_today, df_yesterday]
            return self.__daily_dfs

    def __perform_curl(self, data_type: str) -> str:
        URL = self.API_TYPE_URL['timeseries'] if data_type == 'timeseries' else self.API_TYPE_URL['daily']
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, URL)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.CAINFO, certifi.where())
        c.perform()
        c.close()
        body = buffer.getvalue().decode('utf-8')
        buffer.close()
        return body

    def __process_timeseries_payload(self, payload: str) -> typing.Dict[str, pd.DataFrame]:
        data_dict = json.loads(payload)

        self.population_data_file = os.path.join(self.data_dir, "state-population.json")

        population = None
        
        if os.path.exists(self.population_data_file):
            f = open(self.population_data_file, 'r')
            population = json.loads(json.load(f))
            f.close()
        else:
            payload = self.__perform_curl(data_type='daily')
            daily_dict = json.loads(payload)
            population = {key: value['meta']['population'] for key, value in daily_dict.items()}
            population['UN'] = -1
            f = open(self.population_data_file, 'w')
            json.dump(json.dumps(population), f)
            f.close()

        out_dict = {key: self.__state_ts_df(val['dates'], population[key]) 
                    for key, val in data_dict.items() if key != 'UN'}

        return {
            key: self.__compute_tpr_cfr(value) for key, value in out_dict.items()
        }

    def __state_ts_df(self, state_dict: typing.Dict[str, typing.Dict], population: int) -> pd.DataFrame:
        df = pd.DataFrame(columns=['date'])
        df['date'] = pd.to_datetime(pd.Series(state_dict.keys()))
        df['population'] = pd.Series(np.repeat(population, len(df)))

        df_alt = pd.json_normalize([value for _, value in state_dict.items()])

        return df.join(df_alt)

    def get_all_timeseries(self):
        return self.__all(data_type='timeseries')

    def get_all_daily(self):
        return self.__all(data_type='daily')

    @staticmethod
    def __compute_tpr_cfr(df: pd.DataFrame) -> pd.DataFrame:
        df['tpr'] = 100 * df['delta.confirmed'] / df['delta.tested']
        df['cfr'] = 100 * df['delta.deceased'] / df['delta.confirmed']
        return df


if __name__ == '__main__':
    dl = DataLoader()
    print(dl.get_all_timeseries())
    print(dl.get_all_daily())