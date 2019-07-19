import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from model.reg_field import *
# from config import conf

data=pd.read_csv('./data_history/houseinfo.csv')

# 填充0
data=data.fillna(0)

print(pd.to_numeric(data['search_rate'], errors=0).var())
print(pd.to_numeric(data['search_rate'], errors=0).max())
print(pd.to_numeric(data['search_rate'], errors=0).min())

rate_mapping = {"A": 10, "B": 7.5, "C": 5, "D": 2.5}
data['activity_rate'] = data['activity_rate'].map(rate_mapping)
data['property_rate'] = data['property_rate'].map(rate_mapping)
data['education_rate'] = data['education_rate'].map(rate_mapping)
data['plate_rate'] = data['plate_rate'].map(rate_mapping)
data['search_rate']=round(pd.to_numeric(data['search_rate'], errors=0)/5,3)

data['house_resources']=pd.to_numeric(data['house_resources'].str.split('套').str[0], errors=0)
data['sales_count']=pd.to_numeric(data['sales_count'].str.split('套').str[0], errors=0)

# ------------------- 详细文本维度 start ---------------------- #
data['house_count']=data['basic_info'].str.extract(reg_house_count)
data['struct_type']=data['basic_info'].str.extract(reg_struct_type)
data['green_rate']=data['basic_info'].str.extract(reg_green_rate)
data['volume_rate']=data['basic_info'].str.extract(reg_volume_rate)
data['admin_money']=data['basic_info'].str.extract(reg_admin_money)
data['property_type']=data['basic_info'].str.extract(reg_property_type)
data['safe']=data['basic_info'].str.extract(reg_safe)
data['clean']=data['basic_info'].str.extract(reg_clean)

data['water']=data['amenities_info'].str.extract(reg_water)
data['warm']=data['amenities_info'].str.extract(reg_warm)
data['electric']=data['amenities_info'].str.extract(reg_electric)
data['gas']=data['amenities_info'].str.extract(reg_gas)
data['elevator']=data['amenities_info'].str.extract(reg_elevator)
data['park']=data['amenities_info'].str.extract(reg_park)

#data['park']=data['around_instrument_info'].str.extract(reg_park)

data=data.drop(['basic_info','amenities_info','traffic_info','around_instrument_info'],axis=1) 
'''
data['basic_info'].str.extract(reg)
data['amenities_info']=data['amenities_info'].str.extract(reg)
data['traffic_info']=data['traffic_info'].str.extract(reg)
data['around_instrument_info']=data['around_instrument_info'].str.extract(reg)
'''

# ------------------- 详细文本维度  end  ---------------------- #

# 填充0
data=data.fillna(-1)

data['rate_score']=round(data['activity_rate']+data['property_rate']+data['education_rate']+data['plate_rate']+data['search_rate']+data['sales_count'],3)

data.sort_values(['rate_score'],ascending=False).to_csv('house_score.csv',index=False)


'''
for item in data.sort_values(['rate_score'],ascending=False).iterrows():
    if item[1]['rate_score']>=30:
        print(item[1]['name'],item[1]['rate_score'])
'''











