import csv
import os
from typing import List

from sklearn.preprocessing import MinMaxScaler

class KlineModel:
    def __init__(self, timestamp: int, open_price: float, high_price: float, low_price: float, close_price: float,
                 volume: float, close_time: int, quote_asset_volume: float, num_trades: int,
                 taker_buy_base_asset_volume: float, taker_buy_quote_asset_volume: float, ignore: float):
        self.timestamp = timestamp
        self.feature1 = open_price # open_price
        self.feature2 = high_price # high_price
        self.feature3 = low_price # low_price
        self.feature4 = close_price # close_price
        self.feature5 = volume # volume
        self.close_time = close_time
        self.quote_asset_volume = quote_asset_volume
        self.num_trades = num_trades
        self.taker_buy_base_asset_volume = taker_buy_base_asset_volume
        self.taker_buy_quote_asset_volume = taker_buy_quote_asset_volume
        self.ignore = ignore

    @classmethod
    def from_row(cls, row: List[str]) -> 'KlineModel':
        return cls(
            timestamp=int(row[0]),
            open_price=float(row[1]),
            high_price=float(row[2]),
            low_price=float(row[3]),
            close_price=float(row[4]),
            volume=float(row[5]),
            close_time=int(row[6]),
            quote_asset_volume=float(row[7]),
            num_trades=int(row[8]),
            taker_buy_base_asset_volume=float(row[9]),
            taker_buy_quote_asset_volume=float(row[10]),
            ignore=float(row[11])
        )

    def __str__(self) -> str:
        return f"KlineModel(timestamp={self.timestamp}, open_price={self.feature1}, high_price={self.feature2}, " \
               f"low_price={self.feature3}, close_price={self.feature4}, volume={self.feature5}, " \
               f"close_time={self.close_time}, quote_asset_volume={self.quote_asset_volume}, " \
               f"num_trades={self.num_trades}, taker_buy_base_asset_volume={self.taker_buy_base_asset_volume}, " \
               f"taker_buy_quote_asset_volume={self.taker_buy_quote_asset_volume}, ignore={self.ignore})"

    def __repr__(self) -> str:
        return f"KlineModel(timestamp={self.timestamp}, open_price={self.feature1}, high_price={self.feature2}, " \
               f"low_price={self.feature3}, close_price={self.feature4}, volume={self.feature5}, " \
               f"close_time={self.close_time}, quote_asset_volume={self.quote_asset_volume}, " \
               f"num_trades={self.num_trades}, taker_buy_base_asset_volume={self.taker_buy_base_asset_volume}, " \
               f"taker_buy_quote_asset_volume={self.taker_buy_quote_asset_volume}, ignore={self.ignore})"


class Normalize:
    def __init__(self, feature_indices: List[int]):
        self.feature_indices = feature_indices
        self.scaler = MinMaxScaler()

    def fit_transform(self, data: List[KlineModel]) -> None:
        features = [[getattr(kline, 'feature'+str(idx)) for idx in self.feature_indices] for kline in data]
        self.scaler.fit(features)
        for kline in data:
            normalized_features = self.scaler.transform([[getattr(kline, 'feature'+str(idx)) for idx in self.feature_indices]])
            for idx, feature_idx in enumerate(self.feature_indices):
                setattr(kline, 'feature'+str(feature_idx), normalized_features[0][idx])

    def inverse_transform(self, data: List[KlineModel]) -> None:
        for kline in data:
            normalized_features = [[getattr(kline, 'feature'+str(idx)) for idx in self.feature_indices]]
            inverse_features = self.scaler.inverse_transform(normalized_features)
            for idx, feature_idx in enumerate(self.feature_indices):
                setattr(kline, 'feature'+str(feature_idx), inverse_features[0][idx])




def read_csv(file_path: str) -> List[KlineModel]:
    data: List[KlineModel] = []

    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            model = KlineModel.from_row(row)
            data.append(model)

    return data


# Example usage
folder_path = 'reports'
file_name = 'BTCUSDT_1d_20220101_20220630.csv'
file_path = os.path.join(folder_path, file_name)

if os.path.exists(file_path):
    kline_data = read_csv(file_path)
    normalize = Normalize(feature_indices=[1, 2, 3, 4, 5])  
    normalize.fit_transform(kline_data)
    print(kline_data)
    

else:
    print(f"File '{file_path}' does not exist.")
