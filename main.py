from telethon import TelegramClient, events, sync
from trade_commands import *
import asyncio
import re

api_id = 7937453
api_hash = 'd24973aa7a3311466178b4c3f4952bb6'
client = TelegramClient('anon', api_id, api_hash)
chat = '[VIP] SmartTrader™'


class Ticket:
    def __init__(self, symbol, name, order, modifier=1):
        self.symbol = symbol
        self.name = name
        self.order = order
        self.modifier = modifier


def text_to_ticket(message):
    # If either one is found, then the next line contains an order
    # saves every occurrence of: RAPID/VIP SIGNAL anything (.*) a line break (\s) anything (.*) until line break
    processed_list = re.findall(r'VIP SIGNAL.*\s.*', message) + re.findall(r'RAPID SIGNAL.*\s.*', message)
    # saves occurrences of RAPID UPDATE, as well as the 3 following lines (instead of 1)
    # TODO: add functionality to get all set updates not only the first one in the message
    processed_list = processed_list + re.findall(r'RAPID UPDATE.*\s.*\s.*\s.*', message)
    print(processed_list)
    if len(processed_list) != 0:
        print('Company: ', extract_company(processed_list[0]))

    if message.find('BUY') != -1:  # Using the find() method of a string to look for Buy orders
        pass
        # print(message)


def extract_company(message):  # Takes in a partly processed message containing the type of order and the company
    symbols_list = get_symbols_name()
    result = -1
    for symbol in symbols_list:
        if message.find(symbol) != -1:
            result = symbol
            break
    return result


@client.on(events.NewMessage(chats=chat))
async def my_event_handler(event):
    print(event.raw_text)


async def print_messages():
    dialogs = await client.get_dialogs()
    entity = await client.get_entity(chat)
    print('name: ', entity)
    async for message in client.iter_messages(entity, limit=10):
        text_to_ticket(message.text)
        #print(message.id, message.text)


def main():
    client.start()
    connect()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_messages())
    client.run_until_disconnected()
    loop.close()


if __name__ == '__main__':
    main()


