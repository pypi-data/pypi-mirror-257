import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta

from cagent.modules.client.coingecko_client import CoinGeckoClient
from cagent.modules.client.openai_client import OpenAiClient


class Analyst:
    """
    Analyst is a class mainly used for creaing the analytics report for crypto currency, it can run the following tasks
    - Generate basic report analytics
    - Run the Price Analyitcs
    """

    def __init__(self, id, openai_api_key, coingecko_api_key):
        self.id = id
        self.openai_api_key = openai_api_key
        self.coingecko_api_key = coingecko_api_key
        self.oa_client = OpenAiClient(openai_api_key, max_tokens=1000)
        self.cg_client = CoinGeckoClient(coingecko_api_key)

    def run_metadata_analytics(self, coin):
        metadata_info = self._fetch_coin_metadata_data(coin)
        prompt = self._format_prompt_data(metadata_info)
        result = self.oa_client.query(
            f"I got this the information for {coin}, can you create a summarized introduction? The information is {prompt}"
        )
        return result

    def run_price_analytics(self, coin, days=14):
        coin_price = self._fetch_coin_price_data(coin)
        df_coin_price = self._transform_coin_price_data(coin_price)
        df_filtered = self._filter_data_by_days(df_coin_price, days)

        prompt = self._format_prompt_data(df_filtered)
        result = self.oa_client.query(
            f"I got this the price information for {coin}, can you create a summarized price trends analytics based on the given information? The information is {prompt}"
        )

        return result

    def run_technical_analytics(self, coin, indicators, days=14):
        coin_price = self._fetch_coin_price_data(coin)
        df_coin_price = self._transform_coin_price_data(coin_price)[["date", "price"]]
        df_coin_price.columns = ["date", "close"]
        CustomStrategy = ta.Strategy(
            name="Custom Strategy",
            description="Custom Strategy",
            ta=[{"kind": x} for x in indicators],
        )
        df_strategy_data = df_coin_price.copy()
        df_strategy_data.ta.strategy(CustomStrategy)

        df_filtered = self._filter_data_by_days(df_strategy_data, days)

        prompt = self._format_prompt_data(df_filtered)
        result = self.oa_client.query(
            f"I got this the price information for {coin}, can you create a summarized technical analytics based on the given information? The information is {prompt}"
        )

        return result

    def _filter_data_by_days(self, data, days):
        """
        Filter the data to only within the days to avoid abuse of api
        """
        date_cutoff = datetime.now() - timedelta(days)
        result = data[data["date"] > date_cutoff]
        return result

    def _fetch_coin_metadata_data(self, coin):
        """
        Fetch the single coin price data
        """
        result = self.cg_client.fetch_coins_market_data([coin])[0]
        return result

    def _fetch_coin_price_data(self, coin):
        """
        Fetch the single coin price data
        """
        result = self.cg_client.fetch_coin_price(coin)
        return result

    def _transform_coin_price_data(self, data):
        """
        Transform the coin data from dictionary to pandas dataframe
        """
        # Apply the function to each row
        df = pd.DataFrame(data).apply(self._extract_values, axis=1)
        df.columns = ["date", "price", "market_cap", "volume"]
        return df

    def _extract_values(self, row):
        """
        Function to extract date, price, market cap, and volume
        """
        date = pd.to_datetime(row["prices"][0], unit="ms").normalize()
        price = row["prices"][1]
        market_cap = row["market_caps"][1]
        volume = row["total_volumes"][1]
        return pd.Series([date, price, market_cap, volume])

    def _format_prompt_data(self, data):
        if type(data) == dict:
            formatted_data = []

            for key, value in data.items():
                if "date" in key and value is not None:
                    value = pd.to_datetime(value).strftime("%Y-%m-%d %H:%M:%S")
                elif "image" in key and value is not None:
                    value = f"[Image Link]({value})"

                # Adding formatted line to the list
                formatted_data.append(f"{key.replace('_', ' ').title()}: {value}")

            return "\n".join(formatted_data)
        elif type(data) == pd.core.frame.DataFrame:
            # Start with an introduction
            prompt_friendly_text = [
                "This is the converted information. The DataFrame contains the following columns: "
                + ", ".join(data.columns)
                + "."
            ]

            # Iterate over each column and list their values
            for column in data.columns:
                values = data[column].tolist()
                values_formatted = ", ".join(map(str, values))
                prompt_friendly_text.append(
                    f"The values in '{column}' are: {values_formatted}."
                )

            return " ".join(prompt_friendly_text)
