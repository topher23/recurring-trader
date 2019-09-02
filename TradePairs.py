import Constants as c

class TradePairs:

    def __init__(self, config):

        self.origin = config['orig_currency']
        self.dest = config['dest_currency']
        self.volume = config['volume']

        if (self.origin not in c.currencies):
            raise Exception(self.origin + "is an unsupported currency. Aborting program.")
        if (self.dest not in c.currencies):
            raise Exception(self.dest + "is an unsupported currency. Aborting program.")
