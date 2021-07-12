import asyncio
import websockets
import json
from typing import Dict

from varun_coding import log


class ExchangeWebsockets:
    """
        Base exchange websocket class, implement for individual exchange classes and override as needed
    """

    def __init__(self):
        self.logger = log.setup_custom_logger('websocket_base')

    async def listen(self, uri: str, payload: Dict[str, str]):
        """ Connect to websocket and consume updates """
        async with websockets.connect(uri) as websocket:
            if len(payload):
                await websocket.send(json.dumps(payload))
            while True:
                response = await websocket.recv()
                # Call process_socket_response method with data
                self.process_socket_response(response)

    def subscribe(self, uri: str, payload: Dict[str, str]):
        loop = asyncio.new_event_loop().run_until_complete(self.listen(uri, payload))
        asyncio.set_event_loop(loop)

    def get_websocket_order_book_endpoint(self):
        raise Exception('implement in child')

    def process_socket_response(self, response):
        """
            :param response: Response from websocket feed for exchange
        """
        raise Exception('implement in child')

    def get_socket_order_book(self, symbol, ob):
        """
            Convert order book into style we expect with array of arrays

            Expected result:
            dict(bids=[], asks=[])
            where bids are sorted from low to high, asks are sorted from high to low.

        """
        raise Exception('Implement in child')
