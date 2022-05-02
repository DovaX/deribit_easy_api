import asyncio
import websockets
import json
import hmac
import hashlib
from datetime import datetime
import nest_asyncio
nest_asyncio.apply()


async def call_api(msg,is_testnet=False):
    if is_testnet:
        url='wss://test.deribit.com/ws/api/v2'
    else:
        url='wss://www.deribit.com/ws/api/v2'
    async with websockets.connect(url) as websocket:
        await websocket.send(msg)
        while websocket.open:
            response = await websocket.recv()
            json_par = json.loads(response)
            return(json_par)
 
def run_async_call(msg,is_testnet=False):
    try:
        response = asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg),is_testnet))
    except Exception as e:
        print("Error while accessing API",e)
    return(response)     

class DeribitClient:
    def __init__(self,client_id,client_secret,is_testnet=False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.is_testnet=is_testnet
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
        response=run_async_call(msg,self.is_testnet) 
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
    
    def cancel(self, order_id):
        params = {
            "access_token" : self.access_token,
            "order_id": order_id
        }  

        return self.request("private/cancel", params)


    def cancel_all(self):
        params={"access_token" : self.access_token,
            }
        return self.request("private/cancel_all", params)


    def edit(self, order_id, price, amount):
        params = {
        "access_token" : self.access_token,
        "order_id" : order_id,
        "amount" : amount,
        "price" : price
        }
        return self.request("private/edit", params)


    def get_open_orders(self, instrument="BTC-PERPETUAL"):
        params = {"access_token" : self.access_token,
                  "instrument_name":instrument,
                  }
        return self.request("private/get_open_orders_by_instrument", params)


    def get_positions(self, instrument="BTC-PERPETUAL"):
        params = {"access_token" : self.access_token,
                  "instrument_name":instrument,
                  }
        return self.request("private/get_position", params)


