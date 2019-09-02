import json
from TradePairs import TradePairs

class TradingDetails:

    def __init__(self, config_path):
        with open(config_path) as json_file:
            config = json.load(json_file)

        if config['type'] == 'recurring':
            self.recurring = True
            self.trade_dates = config['trade_date']
            self.trade_time = int(config['trade_time'])
        elif config['type'] == 'single':
            self.recurring = False
            self.trade_dates = "--"
            self.trade_time = "--"
        else:
            raise Exception("Invalid type")

        self.trade_pairs = []
        for pair in config['trade_pairs']:
            self.trade_pairs.append(TradePairs(pair))

    def hi(self):
        print("hi")
