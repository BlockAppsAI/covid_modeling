import numpy as np
import pandas as pd
import os
import pathlib
import datetime as dt
import typing


class ForecastsLoader:
    def __init__(self) -> None:
        self.__forecasts_data: pd.DataFrame = None
        current_file_path = os.path.abspath(__file__)
        path = pathlib.Path(current_file_path)
        
        self.data_dir = 'data'
        for p in path.parents:
            if str(p).endswith('covid_modeling'):
                self.data_dir = os.path.join(p, self.data_dir)
                break

    def get_forecasts(self, compartment='confirmed', forecast_days=7, method='AutoODE', smoothing=None):
        df: pd.DataFrame = None
        if smoothing not in [None, 7]:
            raise ValueError('Smoothing must be None or 7')
        smoothing = str(smoothing) if smoothing is not None else ''
        data_file_path = os.path.join(self.data_dir, f'{method}{smoothing}_{forecast_days}_pred_new.csv')
        forecast_data = pd.read_csv(data_file_path)
        forecast_data['date'] = pd.to_datetime(forecast_data['date'])
        forecast_data.drop(forecast_data.columns.difference(['date', 'delta confirmed', 'delta deceased', 'delta confirmed std', 'delta deseased std']), axis=1, inplace=True)
        return forecast_data


if __name__ == '__main__':
    fl = ForecastsLoader()
    print(fl.get_forecasts())