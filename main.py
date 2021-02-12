from flask import Flask, request, render_template
import json, config
from binance.client import Client
from binance.enums import *

app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET)


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {quantity} - {side} - {symbol} ")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False
    return order


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads((request.data))
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "success",
            "message": "Nice Try See You Madafaking Piece Of S**t"
        }
    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    ticker = data['ticker']
    order_response = order(side, quantity, ticker)
    if order_response:
        return {
            "code": "success",
            "message": "order created successfully"
        }
    else:
        print("order failed")
        return {
            "code": "error",
            "message": "Order Failed"
        }
