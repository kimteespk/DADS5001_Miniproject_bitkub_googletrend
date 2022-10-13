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