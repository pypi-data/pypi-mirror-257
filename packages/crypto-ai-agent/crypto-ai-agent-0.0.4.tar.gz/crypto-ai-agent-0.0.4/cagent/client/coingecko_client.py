import requests
from tqdm import tqdm
from funcy import chunks
import time


class CoinGeckoClient:
    """
    Client for interacting with the CoinGecko API.
    Client doesn't do the job of data transformation it only serves as the middleware to communicate with the node
    """

    def __init__(self, coingecko_api_key):
        self.coingecko_api_key = coingecko_api_key

    def _call_rest_api(self, url):
        """
        Call Rest API and get the response
        """
        request_url = f"{url}x_cg_demo_api_key={self.coingecko_api_key}"
        response = requests.get(request_url)

        # Checking if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Error: Unable to fetch data. Status code:", response.status_code)

    def fetch_coins(self):
        """
        Fetch all the coins list with the metadata information
        """
        result = self._call_rest_api("https://api.coingecko.com/api/v3/coins/list?")
        return result

    def fetch_coin_price(self, coin_id):
        """
        Fetch the single coin price information
        """
        result = self._call_rest_api(
            f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=max&"
        )
        return result

    def fetch_coins_market_data(self, coins, sleeptime=0, chunk_size=250):
        coin_ids_chunks = list(chunks(chunk_size, coins))

        coins_w_market_data = []
        for chunk in tqdm(coin_ids_chunks, desc="Fetching Market Data..."):
            coins_w_market_data.extend(self._fetch_coins_market_data(chunk))
            time.sleep(sleeptime)
        return coins_w_market_data

    def _fetch_coins_market_data(self, coins):
        """
        In Coingecko, there is a 250 limit for the market data fetching, this way is to join the coins list and fetch the data
        """
        ids_param = "%2C%20".join(coins)
        result = self._call_rest_api(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids_param}&order=market_cap_desc&per_page=250&page=1&sparkline=false&locale=en&"
        )
        return result
