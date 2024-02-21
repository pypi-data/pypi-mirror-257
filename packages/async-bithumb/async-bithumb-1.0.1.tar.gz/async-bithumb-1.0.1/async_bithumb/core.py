from errors import AioHttpRequestError, BithumbPrivateError, BithumbPublicError
import asyncio
import base64, urllib, hashlib, hmac, time
import aiohttp


class PublicApi:
    @staticmethod
    async def ticker(order_currency, payment_currency="KRW"):
        try:
            uri = "/public/ticker/{}_{}".format(order_currency, payment_currency)
            return await BithumbHttp().get(uri)
        except AioHttpRequestError as x:
            raise BithumbPublicError(f'{x.__class__.__name__}: {x}')

    @staticmethod
    async def transaction_history(order_currency, payment_currency="KRW", limit=20):
        try:
            uri = "/public/transaction_history/{}_{}?count={}".format(order_currency, payment_currency, limit)
            return await BithumbHttp().get(uri)
        except AioHttpRequestError as x:
            raise BithumbPublicError(f'{x.__class__.__name__}: {x}')

    @staticmethod
    async def orderbook(order_currency, payment_currency="KRW", limit=5):
        try:
            uri = "/public/orderbook/{}_{}?count={}".format(order_currency, payment_currency, limit)
            return await BithumbHttp().get(uri)
        except AioHttpRequestError as x:
            raise BithumbPublicError(f'{x.__class__.__name__}: {x}')

    @staticmethod
    async def btci():
        try:
            uri = "/public/btci"
            return await BithumbHttp().get(uri)
        except AioHttpRequestError as x:
            raise BithumbPublicError(f'{x.__class__.__name__}: {x}')

    @staticmethod
    async def candlestick(order_currency, payment_currency="KRW", chart_intervals="24h"):
        try:
            uri = "/public/candlestick/{}_{}/{}".format(order_currency, payment_currency, chart_intervals)
            return await BithumbHttp().get(uri)
        except AioHttpRequestError as x:
            raise BithumbPublicError(f'{x.__class__.__name__}: {x}')


class PrivateApi:
    def __init__(self, conkey, seckey):
        self.http = BithumbHttp(conkey, seckey)

    async def account(self, **kwargs):
        try:
            return await self.http.post('/info/account', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')

    async def balance(self, **kwargs):
        try:
            return await self.http.post('/info/balance', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')

    async def place(self, **kwargs):
        try:
            return await self.http.post('/trade/place', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')

    async def orders(self, **kwargs):
        try:
            return await self.http.post('/info/orders', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')

    async def order_detail(self, **kwargs):
        try:
            return await self.http.post('/info/order_detail', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')

    async def cancel(self, **kwargs):
        try:
            return await self.http.post('/trade/cancel', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')

    async def market_buy(self, **kwargs):
        try:
            return await self.http.post('/trade/market_buy', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')

    async def market_sell(self, **kwargs):
        try:
            return await self.http.post('/trade/market_sell', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')

    async def withdraw_coin(self, **kwargs):
        try:
            return await self.http.post('/trade/btc_withdrawal', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')
    async def withdraw_cash(self, **kwargs):
        try:
            return await self.http.post('/trade/krw_withdrawal', **kwargs)
        except AioHttpRequestError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')

    async def user_transactions(self, **kwargs):
        try:
            return await self.http.post('/info/user_transactions', **kwargs)
        except BithumbPrivateError as x:
            raise BithumbPrivateError(f'{x.__class__.__name__}: {x}')


class AioHttpMethod:
    def __init__(self, base_url=""):
        self.base_url = base_url

    def update_headers(self, headers):
        self.headers = headers

    async def post(self, path, timeout=3, **kwargs):
        return await self._request('post', path, timeout, **kwargs)

    async def get(self, path, timeout=3, **kwargs):
        return await self._request('get', path, timeout, **kwargs)

    async def _request(self, method, path, timeout, **kwargs):
        try:
            uri = self.base_url + path
            async with aiohttp.ClientSession() as session:
                if hasattr(self, 'headers'):
                    session.headers.update(self.headers)

                task = asyncio.create_task(getattr(session, method)(url=uri, data=kwargs))
                async with await asyncio.wait_for(task, timeout=timeout) as response:
                    resp = await response.json()
            return resp
        except Exception as x:
            raise AioHttpRequestError(f'{x.__class__.__name__}: {x}')


class BithumbHttp(AioHttpMethod):
    def __init__(self, conkey="", seckey=""):
        self.API_CONKEY = conkey.encode('utf-8')
        self.API_SECRET = seckey.encode('utf-8')
        super(BithumbHttp, self).__init__("https://api.bithumb.com")


    def _signature(self, path, nonce, **kwargs):
        query_string = path + chr(0) + urllib.parse.urlencode(kwargs) + \
                       chr(0) + nonce
        h = hmac.new(self.API_SECRET, query_string.encode('utf-8'),
                     hashlib.sha512)
        return base64.b64encode(h.hexdigest().encode('utf-8'))

    async def post(self, path, **kwargs):
        kwargs['endpoint'] = path
        nonce = str(int(time.time() * 1000))

        self.update_headers({
            'Api-Key': (self.API_CONKEY).decode('utf-8'),
            'Api-Sign': (self._signature(path, nonce, **kwargs)).decode('utf-8'),
            'Api-Nonce': nonce
        })
        return await super().post(path, **kwargs)

if __name__ == "__main__":
    print(PublicApi.ticker("BTC"))