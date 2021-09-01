import time

from telethon import TelegramClient, events, sync
import asyncio
import zmq
import pandas
from DWX_ZeroMQ_Connector_v2_0_1_RC8 import *
import os

api_id = 7937453
api_hash = 'd24973aa7a3311466178b4c3f4952bb6'
client = TelegramClient('anon', api_id, api_hash)

zmq = DWX_ZeroMQ_Connector()
order = zmq._generate_default_order_dict()
zmq._DWX_MTX_GET_ALL_OPEN_TRADES_()
print(zmq._thread_data_output)
order['_action'] = 'OPEN'
order['_symbol'] = 'EURUSD'
order['_SL'] = 200
order['_TP'] = 600
order['_comment'] = 'test buy'
order['_lots'] = 0.01

zmq._DWX_MTX_NEW_TRADE_(order)


"""
    try:
        await client.connect()
        print('Connection successful')
    except OSError:
        print('Failed to connect')
"""