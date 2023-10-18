import pyensign
import os
import json
import asyncio
from pyensign.ensign import Ensign

from datetime import datetime
import requests
from pyensign.events import Event
from pyensign.ensign import Ensign
from pyensign.ensign import Ensign

ME = "(https://rotational.io/data-playground/dc-metro, yuchengf@uchicago.edu)"

class CoinCapPublisher_assets:
    def __init__(self, topic="coincap", coincap_key='ddae5c52-2af7-4655-a754-d59d8fb6665a', user=ME):
        self.topic = topic
        self.datatype = "application/json"
        self.url = "https://api.coincap.io/v2/assets/"

        if coincap_key is None:
            self.coincap_key = os.getenv("COINCAP_KEY")
        else:
            self.coincap_key = coincap_key

        if self.coincap_key is None:
            raise Exception("no CoinCap key found; see README section on API key setup")

        self.header = {"User-Agent": user, "api_key": self.coincap_key}

        self.ensign = Ensign(client_id='vXOuRXxlPmFyDzskShlUBLVxlUdtcKjA', client_secret='mzGjsbAJqT479jYGtlvogYipVwFCmhSHmnklXM9Rh0O2PdVsD6YcyDhOFBxm6oyj')

    def unpack_cc_response(self, message):
        coincap_timestamp = message.get("timestamp",None)
        coincap_data = message.get("data", None)
        if coincap_data is None:
            raise Exception("unexpected response from coincap request, no coincap-events found")
        
        for data in coincap_data:
            data_dictionary = {
            'id' : data.get("id",None),
            'price' : data.get("priceUsd",None),
            'timestamp' : coincap_timestamp}

            yield Event(json.dumps(data_dictionary).encode("utf-8"), mimetype=self.datatype)


    async def recv_and_publish(self):
        while True:
            query = self.url
            response = requests.get(query).json()

            # unpack the API response and parse it into events
            events = self.unpack_cc_response(response)
            for event in events:
                await self.ensign.publish(self.topic,event)

            # sleep for a bit before we ping the API again
            await asyncio.sleep(60)



    def run(self):
        """
        Run the publisher forever.
        """
        asyncio.run(self.recv_and_publish())



if __name__ == "__main__":
    publisher = CoinCapPublisher_assets()
    publisher.run()
