import requests
import json
import datetime
import csv
import os
from typing import List, Any, Dict

def download_historical_data(symbol: str, interval: str, start_date: datetime.datetime, end_date: datetime.datetime) -> List[List[Any]]:
    base_url = 'https://api.binance.com/api/v3/klines'
    
    # Convert start_date and end_date to milliseconds
    start_time = int(start_date.timestamp() * 1000)
    end_time = int(end_date.timestamp() * 1000)
    
    params: Dict[str, Any] = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000  # Maximum limit per request
    }
    
    data: List[List[Any]] = []
    while start_time < end_time:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            klines = json.loads(response.text)
            if not klines:
                break
            data.extend(klines)
            start_time = int(klines[-1][0]) + 1
            params['startTime'] = start_time
        else:
            print('Error occurred:', response.status_code)
            break
    
    return data

def save_to_csv(data: List[List[Any]], file_path: str) -> None:
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume',
              'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']   
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

symbol = 'BTCUSDT'  # Symbol for Bitcoin against USDT
interval = '1d'  # Daily interval
start_date = datetime.datetime(2022, 1, 1)
end_date = datetime.datetime(2023, 5, 1)

historical_data = download_historical_data(symbol, interval, start_date, end_date)

folder_path = 'reports'
os.makedirs(folder_path, exist_ok=True)
file_name = f'{symbol}_{interval}_{start_date.strftime("%Y%m%d")}_{end_date.strftime("%Y%m%d")}.csv'
file_path = os.path.join(folder_path, file_name)
save_to_csv(historical_data, file_path)

print(f'Data saved to {file_path}')
