from matplotlib import ticker
import pyupbit
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import pandas as pd

import requests


def get_current_price(tickers):
    price_dict = pyupbit.get_current_price(tickers)
    return price_dict

def get_current_balance(akey,skey):

    access_key = akey
    secret_key = skey
    server_url ="https://api.upbit.com"

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/accounts", headers=headers)

    balance = res.json()
    ticker_box = []
    for b in range(len(balance)):
        ticker=balance[b]['currency']
        ticker="KRW-"+ticker
        ticker_box.append(ticker)

    return balance, ticker_box

def get_list_intersection(list1,list2):
    li = [i for i in list1 if i in list2]
    return li

def get_past_data(ticker,interval,count):
    url = "https://api.upbit.com/v1/candles/minutes/{}?market={}&count={}".format(interval,ticker,count)

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers)
    df = pd.DataFrame(response.json())
    return df