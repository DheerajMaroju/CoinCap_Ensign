import io, json, asyncio, datetime
import pandas as pd
from flask import Flask, request, make_response, send_file, render_template
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
    
@app.route('/asset_selection')
def run_app():
    profits_df = pd.read_csv(r'C:\Users\Dheeraj Maroju\Dropbox\My PC (LAPTOP-9TEPO7IP)\Downloads\data-playground\Coincap\profits.csv')
    prices_df = pd.read_csv(r'C:\Users\Dheeraj Maroju\Dropbox\My PC (LAPTOP-9TEPO7IP)\Downloads\data-playground\Coincap\price_history.csv',header=None)
    prices_df.columns = ["bitcoin", "ethereum", "tether", "binance-coin", "usd-coin", "xrp", "solana", "cardano", "dogecoin", 
    "tron", "multi-collateral-dai", "polygon", "polkadot", "wrapped-bitcoin", "litecoin", "bitcoin-cash", 
    "chainlink", "shiba-inu", "unus-sed-leo", "trueusd", "avalanche", "stellar", "okb", "monero", "uniswap", 
    "ethereum-classic", "binance-usd", "cosmos", "bitcoin-bep2", "filecoin", "internet-computer", "lido-dao", 
    "maker", "crypto-com-coin", "vechain", "quant", "near-protocol", "aave", "stacks", "bitcoin-sv", "the-graph", 
    "algorand", "hedera-hashgraph", "render-token", "tezos", "theta", "the-sandbox", "eos", "axie-infinity", 
    "elrond-egld", "injective-protocol", "decentraland", "thorchain", "xinfin-network", "fantom", "kava", "neo", 
    "paxos-standard", "ecash", "flow", "synthetix-network-token", "zcash", "kucoin-token", "trust-wallet-token", 
    "frax-share", "fei-protocol", "chiliz", "iota", "ocean-protocol", "klaytn", "curve-dao-token", "huobi-token", 
    "rocket-pool", "conflux-network", "mina", "gatetoken", "casper", "ftx-token", "dydx", "gala", "compound", 
    "nexo", "wootrade", "dash", "zilliqa", "loom-network", "basic-attention-token", "1inch", "oasis-network", 
    "arweave", "pancakeswap", "gnosis-gno", "holo", "nem", "aelf", "qtum", "gemini-dollar", "loopring", 
    "convex-finance", "0x"]

    asset = request.args.get('asset')
    if (asset == 'top_5_profitable'):
        profits_df = profits_df.sort_values(by=['Profit'],ascending=False)
        return_dict = {}
        return_dict['message'] = 'top 5 profitable assets'
        count=0
        for i,j in zip(profits_df['Asset'],profits_df['Profit']):
            if count<5:
                return_dict[i]=j
                count+=1
            else:
                break
        return(return_dict)
    elif (asset == 'top_5_loss_making'):
        profits_df = profits_df.sort_values(by=['Profit'])
        return_dict = {}
        return_dict['message'] = 'top 5 loss making assets'
        count=0
        for i,j in zip(profits_df['Asset'],profits_df['Profit']):
            if count<5:
                return_dict[i]=j
                count+=1
            else:
                break
        return(return_dict)
    else: 
        prices, timestamps_num, timestamps_str = [],[],[]

        for i in prices_df[asset]:
            list_ = i.split(',',1)
            price = float(list_[0][1:])
            date = eval(list_[1][:-1]).time()
            date_num = date.hour + date.minute / 60 + date.second / 3600
            formatted_date = '{:02}:{:02}:{:.2f}'.format(date.hour, date.minute, round(date.second + date.microsecond / 1_000_000, 2))
            prices.append(price)
            timestamps_num.append(date_num) 
            timestamps_str.append(formatted_date) 

        predicted_value = float(list(profits_df[profits_df['Asset']==asset]['Prediction'])[0])
        predicted_timestamp = date.hour + (date.minute+1) / 60 + date.second / 3600
        plt.scatter(predicted_timestamp,predicted_value,color='red')

        plt.plot(timestamps_num, prices)
        plt.xlabel('Time')
        plt.ylabel('Price (USD)')
        plt.title(asset)
        plt.xticks(timestamps_num[::30], timestamps_str[::30],rotation=45)
        plt.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        buffer.seek(0)
        return send_file(buffer, mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)