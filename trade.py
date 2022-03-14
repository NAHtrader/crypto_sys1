import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

def trade(akey,skey,side,ticker,wallet):
    access_key = akey
    secret_key = skey
    server_url ="https://api.upbit.com"
    wallet_ticker = ticker[4:]
    if side == "bid":
        query = {
        'market': '{}'.format(ticker),
        'side': 'bid',
        'price': '{}'.format(wallet[wallet_ticker][5]),
        'ord_type': 'price',
        }
    if side == "ask":
        query = {
            'market': '{}'.format(ticker),
            'side': 'ask',
            'volume': '{}'.format(wallet[wallet_ticker][4]),
            'ord_type': 'market',
        }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)