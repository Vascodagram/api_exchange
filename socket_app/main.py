from ast import literal_eval
import redis
import asyncio
import aiohttp
import requests


def get_symbol_kraken():
    res = requests.get('https://api.kraken.com/0/public/AssetPairs')
    data = res.json()['result']
    list_wsname = []
    for i in data:
        list_wsname.append(data[i]['wsname'])
    date_ = {
        "event": "subscribe",
        "pair": list_wsname,
        "subscription": {
            "name": "ticker"
        }
    }
    return date_


async def setup():
    session = aiohttp.ClientSession()
    loop = asyncio.get_event_loop()
    loop.create_task(binance_data('wss://stream.binance.com:9443/ws/!ticker@arr', session))
    loop.create_task(kraken_data('wss://ws.kraken.com/', session))


async def binance_data(url, session):
    async with session.ws_connect(url) as ws:
        try:
            print('Binance connect')
            async for msg in ws:
                await ws.pong()
                for i in literal_eval(msg.data):
                    symbol, price_a, price_b = i['s'], i['a'], i['b']
                    await data_rec('binance', symbol, price_a, price_b)
        except Exception as error:
            print('Binance disconnect', error)


async def kraken_data(url, session):
    async with session.ws_connect(url) as ws:
        try:
            print('Kraken connect')
            await ws.send_json(params)
            async for data in ws:
                data_type = literal_eval(data.data)
                if data.data == '{"event":"heartbeat"}' or type(data_type).__name__ == 'dict':
                    pass
                else:
                    symbol, price_a, price_b = data_type[3], data_type[1]['a'][0], data_type[1]['b'][0]
                    await data_rec('kraken', symbol.replace('/', ''), price_a, price_b)
        except Exception as error:
            print('Kraken disconnect', type(error))


async def data_rec(exchange, symbol, price_a, price_b):
    conn_redis.hset(f'{exchange}_{symbol.lower()}',
                    mapping={"symbol": f"{symbol.lower()}",
                             'price': f"{float(price_a) + float(price_b) / 2}",
                             "exchange": f"{exchange}"})


if __name__ == '__main__':
    params = get_symbol_kraken()
    conn_redis = redis.Redis(host='redis', port=6379, db=0)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())
    loop.run_forever()
