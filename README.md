# Exchange Websocket

## Functionality 
The websocket manager can be used to consume real time order book data and to generate a CSV file for real time trade 
updates of a given currency pair.

## How it works?
Currently, a new instance has to be defined for each currency pair along with the type of websocket channel
(either book or trades). Multiple instances can run together. Flask framework has been used.

**INSTALLATION**:

Clone into your project directory using the following command:
```
git clone https://singhvarun1999@bitbucket.org/cryparb/varun_coding.git
```
Go to the project directory and install Requirements:
```
pip install -r requirements.txt
```
A basic script is given in app.py to run the flask application. However, changes can be made based on the documentation 
below

Run app.py
```
python app.py
```

**GET_ORDER_BOOK**:

The get order book functionality, maintains a live order book based on the data that is received from the websocket. The
user can get the current state of the order book by calling an API endpoint. 

* **Create Instance:**
  
    ```
    book = Bitfinex(symbol="BTC/USD", channel="book")
    ```
    While creating the instance, the user needs to define the symbol: currency pair for which the user wants the order 
    book and the channel: name of the ws channel that the user wants to subscrive to (in this case book).


* **Call Instance:**  
    ```
    book.subscribe(book.get_websocket_orderbook_endpoint(),
                   book.get_subscribe_order_book_payload())
    ```
    Subscribe function will connect to the Bitfinex server, and the order book will be updated in an instance variable


* **Call Endpoint:**
    ```
    http://localhost/book
    ```
    This endpoint will return the current state of the order book. 

**NOTE: The endpoint will return the order book of the currency pair that was defined while creating the instance**


**TRADE_CSV**:

The trade CSV functionality created a CSV file of the trade data for a given currency pair. This CSV is updated in real
time until the process is killed by the user. 

* **Create Instance:**

    ```
    trade = Bitfinex(symbol="BTC/USD", channel="trades", file_path="/Users/varun/Desktop/")
    ```
  While creating the instance, the user needs to define the symbol: currency pair for which the user wants the trade
  data, the channel: name of the ws channel that the user wants to subscribe to (in this case trades), and the file_path:
  the path on where the user wants to create the CSV file. The CSV file that will be generated is called trade.csv


* **Call Instance:**
    ```
    trade.subscribe(trade.get_websocket_orderbook_endpoint(),
                    trade.get_subscribe_order_book_payload())
    ```
  Subscribe function will connect to the Bitfinex server, and the trade data will be written to a CSV file

**NOTE: This will create the trade data csv file of the currency pair that was defined while creating the instance**