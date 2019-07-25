import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from collections import Counter
from collections import OrderedDict
from model.reg_field import *

from sklearn.preprocessing import OneHotEncoder
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
data['build_area']=data['basic_info'].str.extract(reg_build_area)
data['build_count']=data['basic_info'].str.extract(reg_build_count)

data['water']=data['amenities_info'].str.extract(reg_water)
data['warm']=data['amenities_info'].str.extract(reg_warm)
data['electric']=data['amenities_info'].str.extract(reg_electric)
data['gas']=data['amenities_info'].str.extract(reg_gas)
data['elevator']=data['amenities_info'].str.extract(reg_elevator)
data['park']=data['amenities_info'].str.extract(reg_park)
data['communicate']=data['amenities_info'].str.extract(reg_communicate)

# 
data['kindergarten']=data['around_instrument_info'].str.extract(reg_kindergarten)[0].str.split('、').str.len()
data['school']=data['around_instrument_info'].str.extract(reg_school)[0].str.split('、').str.len()
data['university']=data['around_instrument_info'].str.extract(reg_university)[0].str.split('、').str.len()
data['mall']=data['around_instrument_info'].str.extract(reg_mall)[0].str.split('、').str.len()
data['hospital']=data['around_instrument_info'].str.extract(reg_hospital)[0].str.split('、').str.len()
data['postoffice']=data['around_instrument_info'].str.extract(reg_postoffice)[0].str.split('、').str.len()
data['bank']=data['around_instrument_info'].str.extract(reg_bank)[0].str.split('、').str.len()
data['else']=data['around_instrument_info'].str.extract(reg_else)[0].str.split('、').str.len()
data['innersupport']=data['around_instrument_info'].str.extract(reg_innersupport)[0].str.split('、').str.len()


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

# 查看下数据取值区间
# print(Counter(list(data['water'])))
# print(Counter(list(data['warm'])))
# print(Counter(list(data['electric'])))
# print(Counter(list(data['gas'])))
# print(Counter(list(data['elevator'])))
# print(Counter(list(data['park'])))
# print(Counter(list(data['communicate'])))
# print(Counter(list(data['struct_type'])))

# struct_type类型少，可以做onehot编码
# listUniq = data.ix[:,'struct_type'].unique()
# for j in range(len(listUniq)):
#     data.ix[:,'struct_type'] = data.ix[:,'struct_type'].apply(lambda x:j if x==listUniq[j] else x)
# print(data)


# 正在补充房地产知识，找到优劣房源的评估标准
data['rate_score']=round(data['activity_rate']+data['property_rate']+data['education_rate']+data['plate_rate']+data['search_rate'],3) #+data['sales_count']

data.sort_values(['rate_score'],ascending=False).to_csv('house_score.csv',index=False)
















