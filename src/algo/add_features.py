from typing import Callable, List, Tuple

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler


# function to add lags to dataframe
def create_lag_creator(num_lags: int, col_name: str) -> Callable[[pd.DataFrame], pd.DataFrame]:
    def lag_creator(df: pd.DataFrame) -> pd.DataFrame:
        for num in range(num_lags):
            df[f"{col_name}_lag{num + 1}"] = df[col_name].shift(num)
        return df

    return lag_creator


# function to add the label
def add_label_buy_close(df: pd.DataFrame) -> pd.DataFrame:
    df["tomorrow_close"] = df.loc[:, "close"].shift(-1)
    df["label"] = np.where(df.loc[:, "close"] >= df.loc[:, "tomorrow_close"], "SELL", "BUY")
    return df.drop("tomorrow_close", axis=1)


# function to return a dataframe with the columns we want to keep for training
def create_cols_to_keep(list_cols: List[str]) -> Callable[[pd.DataFrame], pd.DataFrame]:
    def cols_to_keep(df: pd.DataFrame) -> pd.DataFrame:
        return df[list_cols]

    return cols_to_keep


# function to split x and y for model
def create_splitter(col_label: str) -> Callable[[pd.DataFrame], Tuple[pd.DataFrame, pd.Series]]:
    def split_x_y(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        df = df.copy()
        x = df.drop(col_label, axis=1)
        y = df[col_label]
        return x, y

    return split_x_y


# simple nan remover
def remove_nans(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()


# add fourier transform features
def create_fourier_transformer(col: str) -> Callable[[pd.DataFrame], pd.DataFrame]:
    def fourier_transform_features(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['fft'] = np.fft.fft(np.asarray(df['close'].tolist()))
        df['absolute'] = df['fft'].apply(lambda x: np.abs(x))
        df['angle'] = df['fft'].apply(lambda x: np.angle(x))
        return df.drop('fft', axis=1)
    return fourier_transform_features
