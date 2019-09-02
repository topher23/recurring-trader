
#Account Key Constants
from enum import Enum

api_key = ''
api_secret = ''.encode()

#URL Constants
base_url = "https://api.sandbox.gemini.com"
heartbeat_url = "/v1/heartbeat"
trades_url = "/v1/mytrades"
balances_url = "/v1/balances"
execute_url = "/v1/order/new"
book_url = "/v1/book/"

#Currency acronyms
currencies = ["btc", "usd", "ltc", "eth", "bch", "zec"]

#sleep for 15 mins
sleep_time_m = 15
sleep_time_s = 900

#order types
fill_or_kill = "fill-or-kill"

#side
buy = "buy"
sell = "sell"

#email
from_address = "cryptoEmail@test.com"
to_address = "topher23@vt.edu"