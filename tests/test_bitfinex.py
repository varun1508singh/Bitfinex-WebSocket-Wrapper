from exchanges.bitfinex import Bitfinex
import unittest


class TestClass(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.test = Bitfinex(symbol="BTC/USD", channel="book")

    def runTest(self):
        pass

    def test_get_endpoint(self):
        assert self.test.get_websocket_orderbook_endpoint() == "wss://api-pub.bitfinex.com/ws/2"

    def test_get_payload(self):
        assert self.test.get_subscribe_order_book_payload() == {
            "event": "subscribe",
            "channel": "book",
            "symbol": "tBTCUSD"
        }

    def test_first_response(self):
        response = [123, [[0.0000886, 1, 1060.55466114], [0.00008859, 1, 1000], [0.00008858, 1, 2713.47159343],
                          [0.00008857, 1, 4276.92870916], [0.00008856, 2, 6764.75562319],
                          [0.00008854, 1, 5641.48532401], [0.00008853, 1, 2255.92632223], [0.0000885, 1, 2256.69584601],
                          [0.00008848, 2, 3630.3], [0.00008845, 1, 28195.70625766],
                          [0.00008844, 1, 15571.7], [0.00008843, 1, 2500], [0.00008841, 1, 64196.16117814],
                          [0.00008838, 1, 7500], [0.00008837, 2, 2764.12999012], [0.00008834, 2, 10886.476298],
                          [0.00008831, 1, 20000], [0.0000883, 1, 1000], [0.00008829, 2, 2517.22175358],
                          [0.00008828, 1, 450.45], [0.00008827, 1, 13000], [0.00008824, 1, 1500], [0.0000882, 1, 300],
                          [0.00008817, 1, 3000], [0.00008816, 1, 100], [0.00008864, 1, -481.8549041],
                          [0.0000887, 2, -2141.77009092], [0.00008871, 1, -2256.45433182],
                          [0.00008872, 1, -2707.58122743],
                          [0.00008874, 1, -5640.31794092], [0.00008876, 1, -29004.93294912], [0.00008878, 1, -2500],
                          [0.0000888, 1, -20000], [0.00008881, 2, -2880.15595827], [0.00008882, 1, -27705.42933984],
                          [0.00008883, 1, -4509.83708214], [0.00008884, 1, -1500], [0.00008885, 1, -2500],
                          [0.00008888, 1, -902.91405442], [0.00008889, 1, -900], [0.00008891, 1, -7500],
                          [0.00008894, 1, -775.08564697], [0.00008896, 1, -150], [0.00008899, 3, -11628.02590049],
                          [0.000089, 2, -1299.7], [0.00008902, 2, -4841.8], [0.00008904, 3, -25320.46250083],
                          [0.00008909, 1, -14000], [0.00008913, 1, -123947.999], [0.00008915, 2, -28019.6]]]
        self.test.channelId = 123

        self.test.process_socket_response(response)
        assert len(self.test.order_book['bid']) == 25
        assert len(self.test.order_book['ask']) == 25

    def test_single_order_response(self):
        update_bid = [123, [0.0000886, 2, 1000]]
        update_ask = [123, [0.00008909, 1, -1000]]
        self.test.process_socket_response(update_bid)
        self.test.process_socket_response(update_ask)
        assert self.test.order_book['bid'][0.0000886], 1000
        assert self.test.order_book['ask'][0.00008909] == -1000

        delete_bid = [123, [0.0000886, 0, 1000]]
        delete_ask = [123, [0.00008909, 0, -1000]]
        self.test.process_socket_response(delete_bid)
        self.test.process_socket_response(delete_ask)
        assert self.test.order_book['bid'][0.0000886] is not True
        assert self.test.order_book['ask'][0.00008909] is not True

        insert_bid = [123, [0.1, 3, 1000]]
        insert_ask = [123, [0.01, 2, -1000]]
        self.test.process_socket_response(insert_bid)
        self.test.process_socket_response(insert_ask)
        assert self.test.order_book['bid'][0.1] is True
        assert self.test.order_book['ask'][0.01] is True


if __name__ == '__main__':
    unittest.main()
