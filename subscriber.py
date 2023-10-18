import json, csv, portalocker, time, os, ast
import asyncio, datetime
from queue import Queue 
import pandas as pd
from river import time_series
from pyensign.ensign import Ensign
from pyensign.api.v1beta1.ensign_pb2 import Nack

class CoincapSubscriber:
    def __init__(self, topic="coincap"):
        self.topic = topic
        self.ensign = Ensign(client_id='vXOuRXxlPmFyDzskShlUBLVxlUdtcKjA', client_secret='mzGjsbAJqT479jYGtlvogYipVwFCmhSHmnklXM9Rh0O2PdVsD6YcyDhOFBxm6oyj')
        self.iterator = 0
        self.prev_date_from_event = ''
        self.asset_profits = []
        self.asset_prices = {}
        self.asset_params = pd.read_csv(r'C:\Users\Dheeraj Maroju\Dropbox\My PC (LAPTOP-9TEPO7IP)\Downloads\data-playground\Coincap\hyperparameters.csv')

    def run(self):
        asyncio.run(self.subscribe())

    async def subscribe(self):
        id_ = await self.ensign.topic_id(self.topic)
        async for event in self.ensign.subscribe(id_):
            await self.handle_event(event)
    
    async def handle_event(self, event):
        try:
            data = json.loads(event.data)
            date_from_event = data['timestamp']

            if self.prev_date_from_event!=date_from_event:
                self.prev_date_from_event = date_from_event
                self.iterator +=1

                # Open the csv file in append mode
                csv_file = 'price_history.csv'
                file_exists_flag = os.path.isfile(csv_file)
                while True:
                    try:
                        with open(csv_file, mode='a', newline='') as file:
                            portalocker.lock(file, portalocker.LOCK_EX)
                            writer = csv.DictWriter(file, fieldnames=self.asset_prices.keys())
                            if not file_exists_flag:
                                writer.writeheader()
                            writer.writerow(self.asset_prices)
                            portalocker.unlock(file)
                        break

                    except:
                        time.sleep(0.5)

                self.asset_prices = {}

                if self.iterator>=25:
                    while True:
                        try:
                            csv_file = 'profits.csv'
                            with open(csv_file, mode='w', newline='') as f:
                                writer = csv.writer(f)
                                writer.writerow(['Asset', 'Prediction', 'Profit'])
                                writer.writerows(self.asset_profits)
                            break
                        except:
                            time.sleep(0.5)

                self.asset_profits = []
            self.generate_model(data)
            
            #print(asset_profits)
        except json.JSONDecodeError:
            print("Received invalid JSON in event payload:", event.data)
            await event.nack(nack.UnknownType)
            return

        #print("New asset received:", data)
        await event.ack()

    def generate_model(self,data):
        asset = data['id']
        asset_params_df = self.asset_params
        try:
            asset_best_params = ast.literal_eval(list(asset_params_df[asset_params_df['asset']==asset]['best_params'])[0])
            p = asset_best_params[0]
            q = asset_best_params[1]
            d = asset_best_params[2]
            m = asset_best_params[3]
        except:
            p,q,d,m = 1,5,2,50

        try:
            price = float(data['price'])
            time = datetime.datetime.fromtimestamp(data['timestamp']/1000)
            self.asset_prices[asset] = (price,time)

            ##getting the predictions
            try:
                globals()[asset+'_model'] = globals()[asset+'_model'].learn_one(price)
            except:
                globals()[asset+'it'] = 0
                globals()[asset+'_past_pred_prices'] = []
                globals()[asset+'_model'] =  time_series.SNARIMAX(p=p,d=d,q=q,m=m)
                globals()[asset+'_model'] = globals()[asset+'_model'].learn_one(price)

            globals()[asset+'it']+=1

            if (globals()[asset+'it']>=20):
                y_pred = globals()[asset+'_model'].forecast(1)[0]
                globals()[asset+'_past_pred_prices'].append(y_pred)
                profit = ((y_pred-price)*100)/price
                self.asset_profits.append((asset,y_pred,profit))
                #print(y_pred,price,asset)

            if (globals()[asset+'it']>=21):
                error = abs(price - globals()[asset+'_past_pred_prices'][0])
                globals()[asset+'_past_pred_prices'].pop(0)

        except:
            pass

        return

if __name__ == "__main__":
    subscriber = CoincapSubscriber()
    subscriber.run()