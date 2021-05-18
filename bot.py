import websocket, json, pprint, talib, numpy

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'icpusdt'
SOCKET = 'wss://stream.binance.com:9443/ws/{}@kline_1m'.format(TRADE_SYMBOL)
closes = []
in_position = False

def on_message(ws, message):
    global closes
    json_message = json.loads(message)
    # pprint.pprint(json_message)
    candle = json_message['k']
    is_candle_close = candle['x']
    close = candle['c']

    if is_candle_close:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all the rsi calculated so far..")
            print(rsi)
            last_rsi = rsi[-1]

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:   
                    print("sell!!")
                    in_position = False
                else:
                    print("You don't have anything to sell")
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("You already bought")
                else:
                    print("buy!!")
                    in_position = True

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("closed") 

def on_open(ws):
    print("opened")

ws = websocket.WebSocketApp(SOCKET,
                              on_open = on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

ws.run_forever()