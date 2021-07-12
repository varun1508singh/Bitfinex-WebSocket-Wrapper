from flask import Flask
from flask_restful import Api
from exchanges.bitfinex import Bitfinex
from threading import Thread

app = Flask(__name__)
api = Api(app)

book = Bitfinex(symbol="BTC/USD", channel="book")
trade = Bitfinex(symbol="BTC/USD", channel="trades", file_path="/Users/varun/Desktop/")


def subscribe_order_book():
    book.subscribe(book.get_websocket_orderbook_endpoint(),
                   book.get_subscribe_order_book_payload())


def create_trade_csv():
    trade.subscribe(trade.get_websocket_orderbook_endpoint(),
                    trade.get_subscribe_order_book_payload())


@app.route('/book', methods=['GET'])
def get_order_book():
    # with the current structure, the parameters in get_socket_order_book function do not change any functionality
    return book.get_socket_order_book('BTC/USD', "ob")


if __name__ == '__main__':
    Thread(target=subscribe_order_book, daemon=True).start()
    Thread(target=create_trade_csv, daemon=True).start()
    app.run()
