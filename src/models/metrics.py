import epyestim.covid19 as covid19
import numpy as np
import pandas as pd
import os
import pathlib
import datetime as dt
import typing

import sys
sys.path.append('../../src')
from consumer import DataLoader


class RtCalculator:

    def __init__(self) -> None:
        self.__rt_data = pd.DataFrame(columns=['date', 'cases', 'R_mean', 'R_var', 'Q0.025', 'Q0.25', 'Q0.5', 'Q0.75', 'Q0.975', 'state'])
        current_file_path = os.path.abspath(__file__)
        path = pathlib.Path(current_file_path)
        
        self.data_dir = 'data'
        for p in path.parents:
            if str(p).endswith('covid_modeling'):
                self.data_dir = os.path.join(p, self.data_dir)
                break

        self.__rt_data_file = os.path.join(self.data_dir, f'rt-{dt.datetime.now().date()}.zip')

        dl = DataLoader()
        self.__data = dl.get_all_timeseries()
        self.si_distribution = covid19.generate_standard_si_distribution()
        self.delay_distribution = covid19.generate_standard_infection_to_reporting_distribution()

    def compute_rt(self) -> None:
        print("Computing... Please wait.")
        for key, df in self.__data.items():
            df.set_index('date', inplace=True)
            df_cases = df['delta.confirmed'].resample('D').mean()
            df_cases[df_cases < 0] = 0
            df_cases.fillna(np.finfo(float).eps, inplace=True)
            df_tvr = covid19.r_covid(df_cases, quantiles=(0.025, 0.25, 0.5, 0.75, 0.975), n_samples=10, smoothing_window=14, r_window_size=7, auto_cutoff=False)
            df_tvr = df_tvr['2020-04-01':]
            df_tvr['state'] = key
            df_tvr.reset_index(inplace=True)
            df_tvr.rename(columns={'index': 'date'}, inplace=True)
            self.__rt_data = self.__rt_data.append(df_tvr)
        # Write file to the data folder
        self.__rt_data.to_csv(self.__rt_data_file, compression={'method': 'zip', 'archive_name': 'rt.csv'}, header=True, index=False)
        print('Done.')


class RtDataLoader:
    def __init__(self) -> None:
        current_file_path = os.path.abspath(__file__)
        path = pathlib.Path(current_file_path)
        
        self.data_dir = 'data'
        for p in path.parents:
            if str(p).endswith('covid_modeling'):
                self.data_dir = os.path.join(p, self.data_dir)
                break

        self.__rt_data_file = os.path.join(self.data_dir, f'rt-{dt.datetime.now().date()}.zip')

    def load_rt(self, state_codes: typing.Union[str, typing.List['str']] = ['KA']) -> typing.Union[pd.DataFrame, typing.Dict[str, pd.DataFrame]]:
        file_name = os.path.basename(self.__rt_data_file)
        if file_name in os.listdir(self.data_dir):
            self.__rt_data = pd.read_csv(self.__rt_data_file, compression='zip')
            states_grouped = self.__rt_data.groupby('state')

            if isinstance(state_codes, list):
                ret_dict = {}
                for state_code in state_codes:
                    ret_dict[state_code] = states_grouped.get_group(state_code)
                return ret_dict
            else:
                return states_grouped.get_group(state_codes)
        else:
            raise ValueError("Latest data not available. Please check later.")


if __name__ == '__main__':
    rtc = RtCalculator()
    rtdl = RtDataLoader()
    rtc.compute_rt()
    print(rtdl.load_rt(['KA']))