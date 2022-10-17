
import pandas as pd
from tvDatafeed import TvDatafeed

tv = TvDatafeed()

# df_bitkub_eth = tv.get_hist('ETHTHB', exchange='BITKUB', n_bars=2000)
# df_bitkub_btc = tv.get_hist('BTCTHB', exchange='BITKUB', n_bars=2000)
# df_bitkub_kub = tv.get_hist('KUBTHB', exchange='BITKUB', n_bars=2000)
# df_bitkub_eth.to_csv('./eth_ohclv_bitkub.csv')
# df_bitkub_btc.to_csv('./btc_ohclv_bitkub.csv')
# df_bitkub_kub.to_csv('./kub_ohclv_bitkub.csv')

df_binance_eth = tv.get_hist('ETHUSDT', exchange='BINANCE', n_bars=2000)
df_binance_btc = tv.get_hist('BTCUSDT', exchange='BINANCE', n_bars=2000)
#df_binance_kub = tv.get_hist('KUBUSDT', exchange='BINANCE', n_bars=2000)
df_binance_eth
#df_binance_kub
df_binance_eth.to_csv('./eth_ohclv_binance.csv')
df_binance_btc.to_csv('./btc_ohclv_binance.csv')

# Return ohlcv in pandas dataframe class






#df.info()
#len(df)

#df_kub = df
#df_btc = df
#df_eth = df


#total_instance = len(df_kub) + len(df_btc) + len(df_eth)
#total_instance + 638