from flask import Flask, render_template, jsonify
import ast
import pandas as pd
import datetime

df = pd.read_csv(r'C:\Users\Dheeraj Maroju\Dropbox\My PC (LAPTOP-9TEPO7IP)\Downloads\data-playground\Coincap\hyperparameters.csv')
print(ast.literal_eval(list(df[df['asset']=='bitcoin']['best_params'])[0])[0])



# profits_df = pd.read_csv(r'C:\Users\Dheeraj Maroju\Dropbox\My PC (LAPTOP-9TEPO7IP)\Downloads\data-playground\Coincap\profits.csv')
# prices_df = pd.read_csv(r'C:\Users\Dheeraj Maroju\Dropbox\My PC (LAPTOP-9TEPO7IP)\Downloads\data-playground\Coincap\price_history.csv',header=None)
# prices_df.columns = ["bitcoin", "ethereum", "tether", "binance-coin", "usd-coin", "xrp", "solana", "cardano", "dogecoin", 
#     "tron", "multi-collateral-dai", "polygon", "polkadot", "wrapped-bitcoin", "litecoin", "bitcoin-cash", 
#     "chainlink", "shiba-inu", "unus-sed-leo", "trueusd", "avalanche", "stellar", "okb", "monero", "uniswap", 
#     "ethereum-classic", "binance-usd", "cosmos", "bitcoin-bep2", "filecoin", "internet-computer", "lido-dao", 
#     "maker", "crypto-com-coin", "vechain", "quant", "near-protocol", "aave", "stacks", "bitcoin-sv", "the-graph", 
#     "algorand", "hedera-hashgraph", "render-token", "tezos", "theta", "the-sandbox", "eos", "axie-infinity", 
#     "elrond-egld", "injective-protocol", "decentraland", "thorchain", "xinfin-network", "fantom", "kava", "neo", 
#     "paxos-standard", "ecash", "flow", "synthetix-network-token", "zcash", "kucoin-token", "trust-wallet-token", 
#     "frax-share", "fei-protocol", "chiliz", "iota", "ocean-protocol", "klaytn", "curve-dao-token", "huobi-token", 
#     "rocket-pool", "conflux-network", "mina", "gatetoken", "casper", "ftx-token", "dydx", "gala", "compound", 
#     "nexo", "wootrade", "dash", "zilliqa", "loom-network", "basic-attention-token", "1inch", "oasis-network", 
#     "arweave", "pancakeswap", "gnosis-gno", "holo", "nem", "aelf", "qtum", "gemini-dollar", "loopring", 
#     "convex-finance", "0x"]


# for i in prices_df['bitcoin']:
#     list_ = i.split(',',1)
#     price = float(list_[0][1:])
#     time_object = eval(list_[1][:-1]).time()
#     date_num = time_object.hour + time_object.minute / 60 + time_object.second / 3600
#     print(time_object,date_num)
#     formatted_time = '{:02}:{:02}:{:.2f}'.format(time_object.hour, time_object.minute, round(time_object.second + time_object.microsecond / 1_000_000, 2))
#     print(formatted_time)

# predicted_value = float(list(profits_df[profits_df['Asset']=='bitcoin']['Prediction'])[0])
# predicted_timestamp = time_object.hour + (time_object.minute+1) / 60 + time_object.second / 3600

# print(predicted_timestamp)