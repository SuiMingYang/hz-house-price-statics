import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC,SVR
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
from sklearn.preprocessing import scale,MinMaxScaler
 
# 时间序列+SVR预测

geography_tree=pd.read_csv("./data_history/geography_tree.csv")
houseprice=pd.read_csv("./data_history/houseprice.csv")
houseinfo=pd.read_csv("./data_history/houseinfo.csv")

'''
for item in houseprice.groupby('name'):
    item[0]
    item[1].
'''
x=[[i,i,i]for i in range(24)]#houseprice[houseprice['name']=='松木场河东']['index']
y=list(houseprice[houseprice['name']=='松木场河东']['price'])



from minepy import MINE
mine = MINE(alpha=0.6, c=15)
mine.compute_score([i for i in range(24)], y)
def print_stats(mine):
    print("MIC:%d" % mine.mic())
    # 1-相关性很高（线性相关，包括正弦，多项式），0-无相关性
print_stats(mine)



scaler = MinMaxScaler(feature_range=(0, 1))
x = scaler.fit_transform(x)

clf = SVR()
clf.fit(x, y)

x=scaler.fit_transform([[i,i,i]for i in range(0,31,1)])
y+=list(clf.predict(scaler.fit_transform(([[i,i,i]for i in range(24,31,1)]))))

plt.plot([i[0] for i in x],y,color='red')
plt.scatter([i[0] for i in x],y,color='blue')
plt.show()

# 收敛问题，用归一化解决





















