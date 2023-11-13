from .util.ToolFunction import *

DEFAULT_NAME = "get_stock_price"
DEFAULT_DESCRIPTION = "Retrieve the latest closing price of a stock using its ticker symbol"

import yfinance as yf


class YahooStocks(ToolFunction):
    def __init__(self, name=DEFAULT_NAME, description=DEFAULT_DESCRIPTION):
        super().__init__(name, description)
        self.add_parameter("symbol", "string", "The ticker symbol of the stock", required=True)
        self.openai_func_desc = self.create_function_dict()

    def run_function(self, symbol: str) -> float:
        print(f"INSIDE FUNCTOIN. Symbol is: {symbol}")
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")['Close'].iloc[-1]
        print("LEAVING FUNCTION")
        return price
    