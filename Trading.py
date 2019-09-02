import Api
from TradingDetails import TradingDetails
import Constants as const
import time as t
from datetime import *
import Email


def run(config_url):
    #Parse config and ensure connection to exchange
    trade_details = TradingDetails(config_url)
    cxn_check()

    if not trade_details.recurring:
        have_required_funds(trade_details.trade_pairs)
        execute_trade(trade_details)
    else:
        while 1:
            while not is_ready_to_trade(trade_details.trade_dates, trade_details.trade_time):
                t.sleep(const.sleep_time_s)
                cxn_check()
            cxn_check()
            have_required_funds(trade_details.trade_pairs)
            execute_trade(trade_details)

def execute_trade(trade_details):
    for trade_pair in trade_details.trade_pairs:
        is_executed = False
        retry_wait_time = 0
        while not is_executed:
            t.sleep(retry_wait_time)
            buy_price = target_buy_price(trade_details)
            if buy_price != -1:
                resp = Api.execute(trade_pair.dest+trade_pair.origin, trade_pair.volume, trade_pair.target_buy_price)
                if resp["is_cancelled"] is "False":
                    is_executed = True
                    print("Trade has executed.")
                    print("Bought " + resp["executed_amount"] + " of " + resp["symbol"] +
                          " at price of " + resp["avg_execution_price"] + " per coin.")
                    Email.success_send(resp)
                else:
                    # If trade was not able to be executed, introduce a wait and try again
                    if retry_wait_time == 0:
                        retry_wait_time = 1
                    elif retry_wait_time > 900:
                        Email.failure_send()
                        raise Exception("Could not execute trade after several spaced out retries. Something must be "
                                        "wrong. Killing program")
                    else:
                        retry_wait_time += 15
                        print("Couldnt execute trade. Tried to buy " + trade_pair.volume + " of " +
                              trade_pair.origin+trade_pair.dest + ". Target buy price was: " + buy_price +
                              " Going to wait " + str(retry_wait_time) + " seconds and retry.")


def target_buy_price(trade_details):
    for trade_pair in trade_details.trade_pairs:
        book = Api.get_book(trade_pair.dest+trade_pair.origin)
        asks = book["asks"]
        ask_book_trade_vol = 0
        for ask in asks:
            ask_book_trade_vol += ask["amount"]
            if ask_book_trade_vol >= trade_pair.volume:
                return ask["amount"]
        return -1




def is_ready_to_trade(trade_dates, trade_time):
    dt = datetime.today()
    if dt.day in trade_dates:
        time_now = int((datetime.now()).strftime('%H%M'))
        print("Current Day: " + str(dt.day) + " Current Time: " + str(time_now))
        print("Configured Day(s): " + str(trade_dates) + " Configured Time: " + str(trade_time))
        if ((time_now + const.sleep_time_m) >= trade_time) and (trade_time-time_now > 0):
            print("Trade window open!")
            return True
        else:
            print("Trade window closed.")
            return False
    else:
        print("It is day "+ str(dt.day) + " of the month. Config is set to trade on "+ str(trade_dates) + " day(s).")
        print("Trade window closed.")
        return False

def have_required_funds(trade_pairs):
    print("Ensuring we have enough funds to make trade")
    balances = Api.funds_query()
    for pair in trade_pairs:
        available_funds = float(balances[pair.origin.upper()])
        if (pair.volume > available_funds):
            raise Exception("There are not enough funds to make trades. Aborting.")
    print("Verified sufficient funds are available.")


def cxn_check():
    print("Ensuring we have stable connection")
    if not Api.is_stable_cxn():
        raise Exception("There is no connection to Gemini. Aborting.")
    print("Stable connection verified")