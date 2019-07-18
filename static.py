import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

data=pd.read_csv('./data_history/houseinfo.csv')

#填充0
data=data.fillna(0)

print()
print(pd.to_numeric(data['search_rate'], errors=0).var())
print(pd.to_numeric(data['search_rate'], errors=0).max())
print(pd.to_numeric(data['search_rate'], errors=0).min())

rate_mapping = {"A": 10, "B": 7.5, "C": 5, "D": 2.5}
data['activity_rate'] = data['activity_rate'].map(rate_mapping)
data['property_rate'] = data['property_rate'].map(rate_mapping)
data['education_rate'] = data['education_rate'].map(rate_mapping)
data['plate_rate'] = data['plate_rate'].map(rate_mapping)
data['search_rate']=pd.to_numeric(data['search_rate'], errors=0)/5

data['house_resources']=pd.to_numeric(data['house_resources'].str.split('套').str[0], errors=0)
data['sales_count']=pd.to_numeric(data['sales_count'].str.split('套').str[0], errors=0)

data['rate_score']=data['activity_rate']+data['property_rate']+data['education_rate']+data['plate_rate']+data['search_rate']+data['sales_count']

data.sort_values(['rate_score'],ascending=False).to_csv('house_score.csv',index=False)
'''
for item in data.sort_values(['rate_score'],ascending=False).iterrows():
    if item[1]['rate_score']>=30:
        print(item[1]['name'],item[1]['rate_score'])
'''











