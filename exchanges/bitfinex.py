import datetime
import pandas as pd
import json
from typing import Dict
from varun_coding.exchanges.websockets_base import ExchangeWebsockets


class Bitfinex(ExchangeWebsockets):
    """
        Bitfinex exchange class to call exchange api methods and consume real-time websocket data
    """

    def __init__(self, symbol="BTC/USD", channel="book", file_path=""):
        self.exchange_name = 'bitfinex'
        super().__init__()
        self.logger.info('Initialized %s' % self.exchange_name)
        self.endpoint = 'wss://api-pub.bitfinex.com/ws/2'
        self.channel_id = 0
        self.channel_name = channel
        self.symbol = symbol
        self.file_path = file_path
        self.len = 25
        self.order_book = {'bid': {}, 'ask': {}}

    def get_websocket_orderbook_endpoint(self) -> str:
        return self.endpoint

    def get_subscribe_order_book_payload(self) -> Dict[str, str]:
        # change self.len if you want to increase the orderbook depth
        payload = {
            "event": "subscribe",
            "channel": self.channel_name,
            "symbol": "t" + self.symbol.replace("/", "")
        }
        return payload

    # def get_subscribe_trades_payload(self):
    #     payload = {
    #         "event": "subscribe",
    #         "channel": "trades",
    #         "symbol": "t" + self.symbol.replace("/", "")
    #     }
    #     return payload

    def process_socket_response(self, response):
        if response is None:
            self.logger.info("Empty data received")
            return
        response = json.loads(response)
        self.data_handler(response)

    def data_handler(self, data):
        if isinstance(data, dict):
            if data['event'] == "info":
                self.logger.info("info message received from server")
            elif data['event'] == "subscribed":
                self.channel_id = data['chanId']
                self.channel_name = data['channel']
                self.logger.info(self.channel_name + " channel has been subscribed")
        elif isinstance(data, list) and data[0] == self.channel_id:
            if self.channel_name == "book":
                self.book_handler(data)
            elif self.channel_name == "trades":
                self.trades_to_csv(data)
        else:
            self.logger.debug("Response data type not supported")

    def book_handler(self, data: list):
        orderInfo = data[1]
        if not orderInfo:
            self.logger.info("No order received")
        if isinstance(orderInfo[0], list):
            self.create_book(orderInfo)
        else:
            self.update_book(orderInfo)

    def create_book(self, data: list):
        if len(data[0]) != 3:
            self.logger.info("Response length not supported")
            return
        # bid_data, ask_data = filter(lambda x: x[2]>0, data), filter(lambda x: x[2] <= 0, data)
        # self.orderBook = {'bid': {order[0]: order[2] for order in bid_data}, 'ask': {order[0]: order[2] for order in ask_data}}
        for order in data:
            if order[2] > 0:
                self.order_book['bid'][order[0]] = order[2]
            else:
                self.order_book['ask'][order[0]] = order[2]

    def update_book(self, data: list):
        if len(data) != 3:
            self.logger.info("Response length not supported")
            return
        count, price, amount = data[1], data[0], data[2]
        side = self.order_book['ask'] if amount < 0 else self.order_book['bid']
        if price in side:
            if count == 0:
                del side[price]
            elif count > 0:
                side[price] = amount
            else:
                self.logger.info("Price already exists but count is negative")
        else:
            if count > 0:
                side[price] = amount
            else:
                self.logger.info("Count not supported and price does not exist " + str(count))

    def get_socket_order_book(self, symbol, ob):
        return {
            "bids": sorted(list(self.order_book['bid'].items()), key=lambda x: x[0], reverse=True),
            "asks": sorted(list(self.order_book['ask'].items()), key=lambda x: x[0])
        }

    def trades_to_csv(self, data: list):
        if self.file_path == "":
            self.logger.info("Path not provided: CSV not created")
            return
        if len(data) >= 2 and data[1] == 'hb':
            self.logger.info("this is not trade data")
            return

        convert = lambda x: datetime.datetime.fromtimestamp(x / 1e3).strftime('%Y-%m-%d %H:%M:%S.%f')
        if len(data) == 2:
            first_df = pd.DataFrame(data[1], columns=["Trade_ID", "Time", "Amount", "Price"])
            first_df['Time'] = first_df['Time'].apply(convert)
            first_df.to_csv(self.file_path + 'trades.csv', index=False, header=True)
        elif len(data) == 3:
            data[2][1] = convert(data[2][1])
            next_df = pd.DataFrame([data[2]])
            next_df.to_csv(self.file_path + 'trades.csv', mode='a', index=False, header=False)
