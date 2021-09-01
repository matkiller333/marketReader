import MetaTrader5 as mt5

accountBD = 8061737
accountFP = 735646


def connect(account=accountFP):
    mt5.initialize()
    authorized = mt5.login(account)

    if authorized:
        print("Connected: Connecting to MT5 Client")
    else:
        print("Failed to connect at account #{}, error code: {}"
              .format(account, mt5.last_error()))
        exit(1)


def open_position(symbol, order_type, size='MED', volume=None):
    symbol_info = mt5.symbol_info(symbol)
    # Finds the appropriate lot size in order to spend accordingly
    if size == 'LOW': investment = 75
    elif size == 'MED': investment = 100
    elif size == 'HIGH': investment = 125
    else: investment = 100

    stop_distance = 5000
    tp_distance = 5000

    if symbol_info is None:
        print(symbol, "not found")
        return

    min_volume = mt5.symbol_info(symbol).volume_min  # Finds the minimum volume required to avoid sending
    max_volume = mt5.symbol_info(symbol).volume_max  # invalid volumes to mt5

    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol, True):
            print("symbol_select({}}) failed, exit", symbol)
            return
    print(symbol, "found!")

    point = symbol_info.point

    if order_type == "BUY":
        order = mt5.ORDER_TYPE_BUY
        # If not specified, sets the volume to invest an amount according to the size variable
        price = mt5.symbol_info_tick(symbol).ask
        if not volume:
            volume = round(investment/price, 2)
            if volume < 0.01: volume = 0.01
        if volume < min_volume:
            volume = min_volume
            print('Could not proceed with a small enough volume to respect price ranges')
        if volume > max_volume:
            volume = max_volume
            print('Could not proceed with a big enough volume to respect price ranges')

        sl = mt5.symbol_info_tick(symbol).bid - (stop_distance * point)
        tp = mt5.symbol_info_tick(symbol).bid + (tp_distance * point)

    elif order_type == "SELL":
        order = mt5.ORDER_TYPE_SELL

        price = mt5.symbol_info_tick(symbol).bid
        if not volume:
            volume = round(investment / price, 2)
            if volume < 0.01: volume = 0.01

        sl = mt5.symbol_info_tick(symbol).ask + (stop_distance * point)
        tp = mt5.symbol_info_tick(symbol).ask - (tp_distance * point)

    else:
        print('Invalid order type, aborting operation')
        return 1

    print('Trading {} points for {}$'.format(volume, price*volume))
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(volume),
        "type": order,
        "price": price,
        "sl": round(sl, 2),
        "tp": round(tp, 2),
        "magic": 123456,
        "comment": "",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    print(request)
    send_request(request)


# To close a position either by ticket, or close all positions of a certain symbol
# TODO: implement a way to sell part of a lot using the volume argument
def close_position_ticket(ticket, volume="ALL"):
    deviation = 20
    print(mt5.positions_get(ticket=ticket))
    order_type = mt5.positions_get(ticket=ticket)[0].type
    if order_type == mt5.ORDER_TYPE_BUY:
        price = mt5.positions_get(ticket=ticket)[0].price_current  # Sell price
    else:
        price = mt5.positions_get(ticket=ticket)[0].price_open  # Buy price

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": mt5.positions_get(ticket=ticket)[0].symbol,
        "volume": mt5.positions_get(ticket=ticket)[0].volume,
        "type": mt5.ORDER_TYPE_SELL,
        "position": ticket,
        "price": price,
        "deviation": deviation,
        "magic": 123456,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    send_request(request)


def close_position_symbol(symbol, volume="ALL"):
    positions = mt5.positions_get(symbol=symbol)
    for position in positions:
        ticket = position.ticket
        close_position_ticket(ticket)


def send_request(request):
    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Failed to send order :(")
        print(result.retcode)
    else:
        print("Order successfully placed!")


# Returns all symbols names that can be traded on the market
def get_symbols_name():
    symbols = mt5.symbols_get()
    name_list = []
    for symbol in symbols:
        name_list.append(symbol.name)
    return name_list


connect()
print(get_symbols_name())
# close_position_ticket(3659385)
# close_position_symbol(symbol='ETHUSD')
# open_position('GOOGLE', 'BUY')
# open_position('ETHUSD', 'BUY')
