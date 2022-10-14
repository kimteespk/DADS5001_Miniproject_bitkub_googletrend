# DADS5001_Miniproject_bitkub_googletrend
# ยอดการค้นหา Google trend ด้วย keyword "Bitkub" จะทำให้ยอด Volume การซื้อขายใน Bitkub สูงขึ้นหรือไม่
# Meme ต่างๆในโลกอินเตอร์เน็ต ส่งผลดีต่อสินค้าและบริการของบริษัทนั้นจริงไหม

ในช่วงหนึ่งที่มี Meme ต่างๆบนโลกอินเตอร์เน็ตมากมาย (ซึ่ง Bitkub ก็เป็นหนึ่งในนั้น) สิ่งหนึ่งที่น่าสนใจคือ มันจะส่งผลบวกต่อสินค้าและบริการของบริษัทนั้นหรือไม่
และด้วยข้อจำกัดการเข้าถึงข้อมูล ที่ไม่สามารถทำให้การค้นคว้านี้มีข้อมูล Daily Active Users ได้ 

จึงได้กลายเป็นความท้าทายขึ้นมาว่า เราจะสามารถใช้ Volume การซื้อขายของเหรียญต่างๆใน Bitkub มาตอบคำถามนี้แทนได้ไหม

# Datasets 
ข้อมูลที่ได้มานั้น ได้มาจากการใช้ Library ช่วยในการดึงข้อมูล
-  ข้อมูลปริมาณการซื้อขายของเหรียญในแต่ละตลาด ใช้ TvDatafeed ซึ่งสามารถใช้ดึงข้อมูลราคาย้อนหลังของเหรียญในตลาดต่างๆ จาก Tradingview
```python

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
```

  - ข้อมูล Google trend ใช้ pytrends ช่วยในการดึงข้อมูล
  ```python
  import pandas as pd

from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)


from pytrends import dailydata
import matplotlib.pyplot  as plt

bitkub = dailydata.get_daily_data('bitkub', 2020, 12, 2022, 9)

# process การืำงานของ function คือมันจะดึงสั้นๆ แบบ daily ที่ละเดือน เพื่อให้อยู่ในcondition ที่จะดึง daily data ของ api 
# จากนั้น นำมา scale และรวม

print(bitkub)


bitkub['bitcoin'].plot()
plt.show()


bitkub.to_csv('./bitkub_trend.csv')
df = pd.DataFrame(bitkub)
  ```
  
  
# ช่วงเวลาของ Datasets ที่ใช้
- ราคาและปริมาณการซื้อขายของเหรียญ
```
----- Bitkub data ------
BTC start date : 2018-05-09
BTC end date : 2022-10-12


ETH start date : 2018-05-09
ETH end date : 2022-10-12


KUB start date 2021-05-20
KUB end date 2022-10-12

----- Binance data ------
BTC start date 2017-08-17 07:00:00
BTC end date 2017-08-17 07:00:00

ETH start date 2017-08-17 07:00:00
ETH end date 2017-08-17 07:00:00
```

- Google Trend
```
<class 'pandas.core.frame.DataFrame'>
Index: 643 entries, 2020-12-01 to 2022-09-04
Data columns (total 5 columns):
 #   Column           Non-Null Count  Dtype  
---  ------           --------------  -----  
 0   bitkub_unscaled  643 non-null    int64  
 1   bitkub_monthly   638 non-null    float64
 2   isPartial        92 non-null     object 
 3   scale            638 non-null    float64
 4   bitkub           638 non-null    float64
dtypes: float64(3), int64(1), object(1)
memory usage: 30.1+ KB
```
# จัดเตรียมข้อมูล

- ข้อมูลที่ใช้นั้น ไม่มี NA แต่สิ่งหนึ่งที่พบคือ ในข้อมูล Google trend นั้น มีข้อมูลเป็น 0 เป็นจำนวนมาก ซึ่งหมายความว่า เมื่อเทียบกับสัดส่วนการค้นหาของวันอื่นๆแล้ว น้อยจนแทบเป็น 0
```python
# count search == 0
not0 = df.loc[df['bitkub'] != 0]
print('Rows bitkub search != 0 :', len(not0))

# Turn days search to percent
days_search_percent = len(not0)/len(df)
print(f'Rows bitkub search per data rows :{days_search_percent:.4f}')

print('Rows bitkub search == 0 :',len(df.loc[df['bitkub'] == 0]))
```
```
Rows bitkub search != 0 : 48
Rows bitkub search per data rows :0.0752
Rows bitkub search == 0 : 590
```
![image](https://user-images.githubusercontent.com/84601005/195844690-ac6108f4-274a-43b9-9886-58aeb3e715d7.png)

- Plot เฉพาะข้อมูลที่ไม่เป็น 0
```
not0['bitkub'].plot()
plt.bar(not0.index, not0['bitkub'])
plt.title('Bitkub search since 2020-12')
plt.show()
```
![image](https://user-images.githubusercontent.com/84601005/195844945-9e38b511-0a25-4077-a4f2-e31ecbcfd2d0.png)

- นำข้อมูลเหรียญที่เตรียมไว้มา Combine กันเพื่อให้พร้อมสำหรับการใช้งาน
```python
# Marge ข้อมูลที่ได้จากตลาด Binance
df_coins_binance = pd.merge(btc_binance, eth_binance, how='left', left_on='datetime', right_on='datetime', suffixes= ['_btc_binance', '_eth_binance'])
df_coins_binance.head()
# Marge ข้อมูลที่ได้จากตลาด Bitkub
df_coins = pd.merge(new_btc, new_eth, how='left', left_on= 'datetime', right_on= 'datetime', suffixes= ['_btc_bitkub', '_eth_bitkub'])
df_coins.head()
```
![image](https://user-images.githubusercontent.com/84601005/195845737-fe3a81fa-e713-458d-93e1-4e3c2b950a11.png)
![image](https://user-images.githubusercontent.com/84601005/195845820-e2f8a663-5b85-44dd-98cb-22149656b972.png)

- ข้อมูลจาก 2 ตลาดยังไม่สามารถทำมา Combine กันได้เนื่องจาก Datetime ของข้อมูลนั้นคนละ Format จึงต้องแปลงให้เป็น datetime type และตัด เวลาออก
```
Binance time  2017-08-17 07:00:00
type binance time <class 'str'>
Biktub time  2018-05-09
type bitkub time <class 'str'>
```
```python
df_coins_binance['datetime'] = pd.to_datetime(df_coins_binance['datetime']).dt.date
type(df_coins_binance['datetime'][0])
df_coins['datetime'] = pd.to_datetime(df_coins['datetime']).dt.date
type(df_coins['datetime'][0])
```

- หลังจากแปลงข้อมูล Datetime เป็นรูปแบบเดียวกันแล้ว จึงสามารถนำมารวมกันได้
```python
df_coins_both = pd.merge(df_coins_binance, df_coins, how= 'inner', left_index=True, right_index= True)
df_coins_both.head(1)
print('rows binance before concat ', len(df_coins_binance))
print('rows bitkub before concat ', len(df_coins))

print('\nrows after concat ', len(df_coins_both))
print('NA row in bitkub data', df_coins_both['volume_btc_bitkub'].isna().sum())
```
```
rows binance before concat  1884
rows bitkub before concat  1618

rows after concat  1618
NA row in bitkub data 0
```
- ได้ Dataframe ใหม่ที่มีข้อมูลรวมทุกตลาด
```python
# นำมาจัดเรียงเฉพาะ Column ที่ต้องการใช้
df_coins = df_coins_both[[ 'volume_btc_binance', 'volume_eth_binance', 'volume_btc_bitkub', 'volume_eth_bitkub']]
df_coins
```
```
volume_btc_binance	volume_eth_binance	volume_btc_bitkub	volume_eth_bitkub
datetime				
2018-05-09	25673.524899	112353.37758	2.132158	18.387816
2018-05-10	25055.063718	102019.29933	0.536473	4.644577
2018-05-11	48227.048061	216953.54991	1.889688	8.693208
2018-05-12	40241.320810	166801.07487	0.231786	6.635473
2018-05-13	25632.869362	136022.39207	1.817175	7.472291
...	...	...	...	...
2022-10-08	102480.098420	203391.66120	69.469531	855.087887
2022-10-09	113900.826810	186201.91850	68.305813	899.807182
2022-10-10	212509.098490	393663.01140	88.753887	1072.780040
2022-10-11	243443.070480	429430.39410	89.960297	1364.960923
2022-10-12	213801.546740	369712.57590	49.534364	666.621004
```


- เปลี่ยน column datetime ของข้อมูล google trend ให้เป็นรูปแบบเดียวกับราคา
```python
df.reset_index(inplace= True)
df['date'] = pd.to_datetime(df['date']).dt.date
type(df['date'][0])
```
- นำข้อมูล Google trend และ ข้อมูลของเหรียญ ที่เตรียมไว้มารวมกันตามวันที่
```python
df_joined = pd.merge(df, df_coins, how='left', left_on='date', right_on= 'datetime')
df_joined.rename(columns={'date': 'datetime'}, inplace= True)
df_joined.set_index('datetime', inplace= True)
df_joined

# filter มาแค่ Column ที่ใช้
df_joined_base = df_joined.iloc[:, 4:]
#df_joined_base
df_joined_base.rename(columns={'bitkub': 'googletrend'}, inplace= True)
df_joined_base
```

```
	googletrend	volume_btc_binance	volume_eth_binance	volume_btc_bitkub	volume_eth_bitkub
datetime					
2020-12-06	0.0	37043.091861	602496.96339	145.801752	1692.904166
2020-12-07	0.0	41372.296293	498329.37589	165.108189	1606.013348
2020-12-08	0.0	61626.947614	804443.00717	307.878653	3049.675731
2020-12-09	0.0	79585.553801	997192.16738	638.214088	5347.911585
2020-12-10	0.0	52890.675094	608414.51466	277.778894	1840.982009
...	...	...	...	...	...
2022-08-31	0.0	276946.607650	949227.67750	142.028756	4506.912619
2022-09-01	0.0	245289.945760	728710.48200	115.642678	3859.938572
2022-09-02	0.0	245986.603300	919009.65980	144.389379	3877.928573
2022-09-03	0.0	146639.032040	321397.21890	102.685741	2868.586379
2022-09-04	0.0	145588.778930	296591.11660	83.215608	1508.475600
638 rows × 5 columns
```

# จัดการกับข้อมูลเพื่อที่จะนำมาใช้หาคำตอบ

- นำข้อมูลด้าน ปริมาณการซื้อขายต่อวันมาเปลี่ยนเป็น อัตราการเปลี่ยนแปลงไปจากวันที่ n ต่อวันที่ n+1

```python
# สร้าง list ของชื่อ Column ที่ต้องการเพื่อนำมาคำนวนด้วย for loop
all_col = df_joined_base.columns[1:]

# คำนวนอันตราการเปลี่ยนแปลงแบบ n+1, n+3, n+7 และ shift ข้อมูลกลับมาเป็นวันที่ n เพื่อให้ตรงกับวันที่เกิดการค้นหาใน google 
# เพื่อที่จะได้นำมาเปรียบเทียบว่าวันที่มีการค้นหานั้น ทำให้ปริมาณการซื้อขาย(volume) ในช่วงเวลานั้นมีการเปลี่ยนแปลงหรือไม่
for i in all_col:
    #print(i+'_1d_chg')
    df_joined[i+'_1d_chg'] = df_joined[i].pct_change(1).shift(-1)
    df_joined[i+'_1d_chg'] = df_joined[i+'_1d_chg']#.abs()
    
    df_joined[i+'_3d_chg'] = df_joined[i].pct_change(3).shift(-3)#.abs()
    df_joined[i+'_7d_chg'] = df_joined[i].pct_change(7).shift(-7)#.abs()
df_joined
```

- Plot เพื่อดู %chg ของ Volume เทียบกับ Google trend 
```python
pp = sns.pairplot(df_joined[['googletrend', 'volume_btc_bitkub_1d_chg', 'volume_eth_bitkub_1d_chg']])
pp.fig.suptitle('1 Day percent change of volume at bitkub')

plt.show()
```
![image](https://user-images.githubusercontent.com/84601005/195848549-cdca19ca-03ae-4665-a51b-191b6c0e61ce.png)
- ข้อมูลที่ Google trend เป็น 0 เยอะมาก จึง Filter != มาเพื่อ Plot อีกครั้ง
![image](https://user-images.githubusercontent.com/84601005/195848694-4598bae3-26db-4735-ad74-238de2068ef2.png)
- ข้อมูลของ Google trend ไม่สามารถอธิบายถึงการเปลี่ยนแปลงของของปริมาณการซื้อขายได้ เพราะแต่ละเหรียญนั้นมีปัจจัยอื่นๆที่ส่งผลต่อปริมาณการซื้อขาย จึงไม่สามารถใช้แทน Daily active users ได้ อย่างที่คาดการณ์ไว้


- ลองดู Corrletation ของข้อมูล
```python
df_joined_searched[['googletrend', 'volume_btc_bitkub_1d_chg', 'volume_eth_bitkub_1d_chg']].corr().iloc[0]
```

```
googletrend                 1.000000
volume_btc_bitkub_1d_chg    0.017134
volume_eth_bitkub_1d_chg    0.101641
Name: googletrend, dtype: float64
```

- ลองใช้การค่าเฉลี่ยของการเปลี่ยนแปลงจากทั้ง2เหรียญตัวอย่าง และนำมาเปรียบเทียบกันตลาด Binance เพื่อลดการเปลี่ยนแปลงของปริมาณการซื้อขายที่เกิดจากปัจจัยอื่นๆของตัวเหรียญ
```python
# สร้าง Dataframe ใหม่ และนำมาหาคาเฉลี่ยการเปลี่ยนแปลงของทั้ง 2 เหรียญ ของวันทั้งหมด
df_mean = pd.DataFrame()
df_mean['googletrend'] = df_joined['googletrend']
df_mean['binance_avg_1d_chg'] = df_joined[['volume_btc_binance_1d_chg', 'volume_eth_binance_1d_chg']].mean(axis=1)
df_mean['bitkub_avg_1d_chg'] = df_joined[['volume_btc_bitkub_1d_chg', 'volume_eth_bitkub_1d_chg']].mean(axis=1)
total_percent = (df_mean['binance_avg_1d_chg'] < df_mean['bitkub_avg_1d_chg']).sum()/len(df_mean)
df_mean.reset_index(inplace= True)

plt.scatter(df_mean['bitkub_avg_1d_chg'], df_mean['binance_avg_1d_chg'], c= df_mean['googletrend']
            , alpha= 0.5)
plt.xlabel('Average change of volume at bitkub')
plt.ylabel('Average change of volume at binance')
plt.show()
```
![image](https://user-images.githubusercontent.com/84601005/195849294-acfd44b6-1f64-4f06-9ac7-8020b1549fac.png)
- มี Outlier ในฝั่งของตลาด Bitkub จึงทำไม่เห็นข้อมูลที่ต้องการ

```python
# เช็ค Outlier และตัดทิ้ง
display(df_mean.loc[df_mean['bitkub_avg_1d_chg']>20])
df_mean_cut_outlier = df_mean.loc[df_mean['bitkub_avg_1d_chg'] < 20]
#display(df_mean_cut_outlier.loc[df_mean_cut_outlier['bitkub_avg_1d_chg']] > 10)
```

```
	datetime	googletrend	binance_avg_1d_chg	bitkub_avg_1d_chg
44	2021-01-19	0.0	0.048178	152.445395
```

```python
plt.scatter(df_mean_cut_outlier['bitkub_avg_1d_chg'], df_mean_cut_outlier['binance_avg_1d_chg'], s= df_mean_cut_outlier['googletrend'], alpha= 0.8)#, cmap= 'jet')
#cb = plt.colorbar()
plt.xlabel('Average change of volume at bitkub')
plt.ylabel('Average change of volume at binance')
plt.show()
```
![image](https://user-images.githubusercontent.com/84601005/195849725-6e4ca62e-fec1-4a22-8056-f4efd37fb31f.png)
- การเปลี่ยนแปลงด้านปริมาณของทั้ง 2 ตลาดมีความไกล้เคียงกันมาก จึงจะทำข้อมูลจากทั้ง 2 ตลาดมาเปรียบเทียบกัน เพื่อที่จะได้เห็นมิติอื่นๆจากข้อมูลชุดนี้

- ลองเปรียบเทียบ % ของจำนวนวัน ที่ การเปลี่ยนแปลงของ Volume ใน Bitkub สูงกว่า ใน Binance
  - สร้าง Dataframe ใหม่ และนำมาหาคาเฉลี่ยการเปลี่ยนแปลงของทั้ง 2 เหรียญ เฉพาะวันที่การค้นหาเป็น 0
 
```python
df_mean_no_searched = pd.DataFrame()
df_mean_no_searched = df_joined.loc[(df_joined['googletrend'] == 0)]
df_mean_no_searched['binance_avg_1d_chg'] = df_mean_no_searched[['volume_btc_binance_1d_chg', 'volume_eth_binance_1d_chg']].mean(axis=1)
df_mean_no_searched['bitkub_avg_1d_chg'] = df_mean_no_searched[['volume_btc_bitkub_1d_chg', 'volume_eth_bitkub_1d_chg']].mean(axis=1)
no_search_percent = (df_mean_no_searched['binance_avg_1d_chg'] < df_mean_no_searched['bitkub_avg_1d_chg']).sum()/len(df_mean)
```

  - สร้าง Dataframe ใหม่ และนำมาหาคาเฉลี่ยการเปลี่ยนแปลงของทั้ง 2 เหรียญ ของวันทั้งหมด เฉพาะวันที่มีการค้นหา
```python
df_mean_searched = pd.DataFrame()
df_mean_searched['googletrend'] = df_joined_searched['googletrend']
df_mean_searched['binance_avg_1d_chg'] = df_joined_searched[['volume_btc_binance_1d_chg', 'volume_eth_binance_1d_chg']].mean(axis=1)
df_mean_searched['bitkub_avg_1d_chg'] = df_joined_searched[['volume_btc_bitkub_1d_chg', 'volume_eth_bitkub_1d_chg']].mean(axis=1)
df_mean_searched['excess_avg_1d_chg'] = df_mean_searched['bitkub_avg_1d_chg'] - df_mean_searched['binance_avg_1d_chg']

search_percent = (df_mean_searched['binance_avg_1d_chg'] < df_mean_searched['bitkub_avg_1d_chg']).sum()/len(df_mean_searched)
```

 - Plot เทียบระหว่าง Google trend และ การเปลี่ยนแปลงของปริมาณการซื้อขาย เฉพาะวันที่ การเปลี่ยนแปลงใน Bitkub สูงกว่าใน Binance
 
```python
width = 0.3
mpl.rcParams['figure.figsize'] = [10, 5]


fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax2.set_ylim(0)

df_mean_searched.googletrend.plot(kind= 'bar', ax= ax1, width= width, position=1)
#df_mean_searched.bitkub_avg_1d_chg.plot(kind= 'bar', color= 'r', ax= ax2, width= width, position=0)
df_mean_searched.bitkub_avg_1d_chg.loc[df_mean_searched['bitkub_avg_1d_chg'] > df_mean_searched['binance_avg_1d_chg']].plot(kind= 'bar', color= 'r', ax= ax2, width= width, position=0)

ax1.set_title('Google trend search and Volume percent change (Filter: Bitkub volume change > Binance volume change)')


ax1.set_ylabel('Google Trend')
ax2.set_ylabel('Volume percent change')
ax1.set_xlabel('Days')

plt.show()
```
![image](https://user-images.githubusercontent.com/84601005/195850767-6fa509e4-a173-4278-904a-4195d69737dd.png)


```python
mpl.rcParams['figure.figsize'] = [5, 5]
plt.scatter(df_mean_cut_outlier['bitkub_avg_1d_chg'] - df_mean_cut_outlier['binance_avg_1d_chg'], df_mean_cut_outlier['googletrend'], alpha= 0.8)
#cb = plt.colorbar()
plt.xlabel('Average change of volume at bitkub')
plt.ylabel('Googletrend')
plt.show()
```
- จากรูปยังไม่ได้คำตอบที่แน่ชัด เพราะมีทั้งวันที่มีการค้นหามากและปริมาณการซื้อขายเพิ่มขึ้นมาก แต่ยังมีวันที่มีการค้นหามาก แต่ปริมาณการซื้อขายที่ Bitkub ไม่ได้เพิ่มขึ้นเมื่อเทียบกับ Binance

- ดูสัดส่วนว่าในวันทั้งหมด, วันที่มีการค้นหา, วันที่ไม่มีการค้นหา มีอัตราส่วนเท่าไหร่ ที่ปริมาณการซื้อขายใน Bitkub เปลี่ยนแปลงเพิ่มขึ้นมากกว่า ปริมาณการซื้อขายใน Binance

```python
print(f'Percent of days volume change at bitkub > volume change at binance :{total_percent:.4f}')
print(f'Percent of days volume change at bitkub > volume change at binance (Search == 0) :{no_search_percent:.4f}')
print(f'Percent of days volume change at bitkub > volume change at binance (Search != 0) :{search_percent:.4f}')

mpl.rcParams['figure.figsize'] = [5, 5]
plt.title('Percent volume change (bitkub > binance)')
plt.bar('Whole data' ,total_percent)
plt.bar('Search == 0',no_search_percent)
plt.bar('Search != 0', search_percent)
plt.ylabel('Ratio days bitkub %chg > binance %chg per total days')
plt.show()
```

```
Percent of days volume change at bitkub > volume change at binance :0.4875
Percent of days volume change at bitkub > volume change at binance (Search == 0) :0.4357
Percent of days volume change at bitkub > volume change at binance (Search != 0) :0.6875
```
![image](https://user-images.githubusercontent.com/84601005/195851079-c8af79b9-f67b-492c-bf78-48bcda996c68.png)

- สรุปได้ว่าถึงแม้การเปลี่ยนแปลงของปริมาณการซื้อขาย จะไม่มีความผันแปรต่อยอดการค้นหาเลย "แต่เมื่อดูจากกราฟด้านบน ในวันที่มีการค้นหาใน Google การเปลี่ยนแปลงของปริมาณการซื้อขายเฉลี่ยของทั้ง 2 เหรียญในตลาด Bitkub สูงกว่า ตลาด Binance ถึง 68.75% ของวันทั้งหมดที่มีการค้นหา
แต่ในวันที่ไม่มีการค้นหาใน Google นั้น สูงกว่าเพียงแค่ 43.57% ของวันทั้งหมดที่ไม่มีการค้นหา

# Question & Answer
- กระแสสังคมที่เกิดขึ้นในโลกอินเตอร์เน็ต และการค้นหาใน Google ทำให้เกิดผลบวกต่อบริษัท ซึ่งจากโปรเจ็คนี้ สะท้อนมาในรูปแบบของ Volume การซื้อขายของเหรียญใน Bitkub
- การใช้ข้อมูลของตลาดอื่น (Binance) มาช่วยลดปัจจัยที่ส่งผลต่อปริมาณการซื้อขายในตลาดที่ต้องการจะทดสอบ (Bitkub)  สามารถทำได้

# Challenge ที่พบในการทำ Mini-Project นี้
- การนำข้อมูลที่ไม่ใด้เหมาะสมกับคำถามที่สุดมาใช้ การใช้ Volume การซื้อขาย (แทนที่จะเป็น Daily Active Users โดยตรง) วิเคราะห์ร่วมกับ Google Trend สามารถทำได้อย่างยากลำบาก โดยในกรณีนี้ นำข้อมูลจาก Binance มาช่วย




