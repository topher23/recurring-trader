import requests
import json
import base64
import hmac
import hashlib
import datetime, time
import Constants as const


def is_stable_cxn():
    response = private_simple_api_hit(const.heartbeat_url)
    if response['result'] == 'ok':
        return True
    else:
        print("Connection could not be established. Printing response")
        print(response)
        return False


def get_book(pair):
    return public_external_call(const.book_url + pair)

def execute(symbol, volume, price):
    nonce = create_nonce()
    payload = { "request": const.execute_url,
                "nonce": nonce,
                "symbol": symbol,
                "amount": volume,
                "price": price,
                "side": const.buy,
                "type": const.fill_or_kill
              }
    return private_api_hit(const.execute_url, payload)


def funds_query():
    response = private_simple_api_hit(const.balances_url)
    balances = {}
    for object in response:
        balances[object['currency']] = object['available']
    return balances

def private_api_hit(req_url, payload):
    request_headers = encode_payload(payload)
    return private_external_call(req_url, request_headers)


def private_simple_api_hit(req_url):
    nonce = create_nonce()
    payload = {"request": req_url, "nonce": nonce}
    request_headers = encode_payload(payload)
    return private_external_call(req_url, request_headers)


def create_nonce():
    return str(int(time.time() * 1000))


def encode_payload(payload):
    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(const.api_secret, b64, hashlib.sha384).hexdigest()
    request_headers = {
        'Content-Type': "text/plain",
        'Content-Length': "0",
        'X-GEMINI-APIKEY': const.api_key,
        'X-GEMINI-PAYLOAD': b64,
        'X-GEMINI-SIGNATURE': signature,
        'Cache-Control': "no-cache"
    }
    return request_headers

def public_external_call(req_url):
    return requests.get(const.base_url + req_url).json()

def private_external_call(req_url, request_headers):
    return requests.post(const.base_url + req_url, headers=request_headers).json()