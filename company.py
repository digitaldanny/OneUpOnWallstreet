import utils
from pandas import DataFrame

class Company:
    def __init__(self, ticker):
        self.ticker = ticker
        self.financial_dataframe = DataFrame()
        self.num_years = 0
        self.frequency = "NA"

    def collect_financial_data(self, num_years, frequency):
        '''
        Collect financial data of the company for the specified number of years / frequency and store that data
        into a dataframe.
        '''
        utils.needsImplementation()

    def calculate_price_earnings_ratio(self):
        utils.needsImplementation()

    def calculate_top_selling_items(self, ticker):
        utils.needsImplementation()