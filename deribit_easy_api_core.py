import asyncio
import websockets
import json
import hmac
import hashlib
from datetime import datetime
import nest_asyncio
nest_asyncio.apply()

async def call_api(msg):
    async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
        await websocket.send(msg)
        while websocket.open:
            response = await websocket.recv()
            json_par = json.loads(response)
            return(json_par)
 
def run_async_call(msg):
    try:
        response = asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
    except Exception as e:
        print("Error while accessing API",e)
    return(response)     

class DeribitClient:
    def __init__(self,client_id,client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        auth=self.authenticate()
        self.access_token=auth["result"]["access_token"]
        
    def authenticate(self):                
        timestamp = round(datetime.now().timestamp() * 1000)
        nonce = "abcd"
        data = ""
        signature = hmac.new(
            bytes(self.client_secret, "latin-1"),
            msg=bytes('{}\n{}\n{}'.format(timestamp, nonce, data), "latin-1"),
            digestmod=hashlib.sha256
        ).hexdigest().lower()
        params={
            
            "grant_type" : "client_signature",
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "timestamp" : timestamp,
            "signature" : signature,
            "nonce" : nonce,
            "data" : data,
            "scope":"trade:read_write session:mysessionname"
          }
        
        response=self.request("public/auth",params=params)
        return(response)

        
    def request(self,method,params):
        
        msg = {
          "jsonrpc" : "2.0",
          "id" : 1,
          "method" : method,
          "params" : params
        }
        response=run_async_call(msg) 
        return(response)


    def limit_buy(self,price,amount,post_only=False):
        params={
            "access_token" : self.access_token,
            "instrument_name" : "BTC-PERPETUAL",
            "amount" : amount,
            "price": price,
            "type" : "limit",
            "post_only": post_only,
            "reject_post_only": post_only,
            "label" : "algoorder"
          }
        response=self.request("private/buy",params)
        return(response)

    def market_buy(self,amount):
        params={
            "access_token" : self.access_token,
            "instrument_name" : "BTC-PERPETUAL",
            "amount" : amount,
            "type" : "market",
            "label" : "algoorder"
          }
        response=self.request("private/buy",params)
        return(response)

    def limit_sell(self,price,amount,post_only=False):
        params={
            "access_token" : self.access_token,
            "instrument_name" : "BTC-PERPETUAL",
            "amount" : amount,
            "price": price,
            "type" : "limit",
            "post_only": post_only,
            "reject_post_only": post_only,
            "label" : "algoorder"
          }
        response=self.request("private/sell",params)
        return(response)

    def market_sell(self,amount):
        params={
            "access_token" : self.access_token,
            "instrument_name" : "BTC-PERPETUAL",
            "amount" : amount,
            "type" : "market",
            "label" : "algoorder"
          }
        response=self.request("private/sell",params)
        return(response)


