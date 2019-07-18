import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import learning_curve
from sklearn.metrics import precision_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import recall_score

geography_tree=pd.read_csv("./data/geography_tree.csv")
houseprice=pd.read_csv("./data/houseprice.csv")
houseinfo=pd.read_csv("./data/houseinfo.csv")
'''
print(len(houseprice.groupby('name')))
for house in houseprice.groupby('name'):
    print(house[0])
    #house[0] 小区时序房价数据
'''
try:
    #清洗数据
    for i,house in houseinfo.iterrows():
        #print(house['name'])
        

        '''
        house["name"]
        house["house_resources"]
        house["sales_count"]

        house["activity_rate":]
        house["property_rate"]
        house["education_rate"]
        house["plate_rate"]

        house["search_rate"]

        house["basic_info"]
        house["amenities_info"]
        house["traffic_info"]
        house["around_instrument_info"]
        '''

        basic_info_obj={}
        amenities_info_obj={}
        traffic_info_obj={}
        around_instrument_info_obj={}

        # 清洗数据的不确定性，全部场景都要考虑到
        if house["basic_info"].find('\n')>-1:
            for key in house["basic_info"].split('\n'):
                basic_info_obj[key.split('：')[0].replace(" ","")]=key.split('：')[1]

            for key in house["amenities_info"].split('\n'):
                amenities_info_obj[key.split('：')[0].replace(" ","")]=key.split('：')[1]
                
            for key in house["traffic_info"].split('\n'):
                traffic_info_obj[key.split('：')[0].replace(" ","")]=key.split('：')[1]

            for key in house["around_instrument_info"].split('\n'):
                around_instrument_info_obj[key.split('：')[0].replace(" ","")]=key.split('：')[1]
            
        else:
            #补全代码
            pass
except Exception as e:
    print(e)

print(basic_info_obj)
print(amenities_info_obj)
print(traffic_info_obj)
print(around_instrument_info_obj)



#数据数值化，归一化

























