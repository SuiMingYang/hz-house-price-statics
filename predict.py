import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

data = pd.read_csv('./data_history/houseprice.csv')

data=data[data['name']==u'王家弄小区']
x=list(data['date','price'])
y=list(data['date','price'])

# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

# warnings.filterwarnings("ignore") # specify to ignore warning messages

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)

            results = mod.fit()

            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except Exception as e:
            print(e)
            continue

mod = sm.tsa.statespace.SARIMAX(y,
                                order=(1, 1, 0),
                                seasonal_order=(1, 0, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

results = mod.fit()

print(results.summary().tables[1])



pred = results.get_prediction(start=pd.to_datetime('2019-07'), dynamic=False)
pred_ci = pred.conf_int()

'''
data = pd.read_csv('./data_history/houseprice.csv', parse_dates=['date'], index_col='index')
#差分处理
diff_series = diff_series.diff(1)#一阶
diff_series2 = diff_series.diff(1)#二阶
#ACF与PACF
#从scipy导入包
from scipy import stats
#画出acf和pacf
sm.graphics.tsa.plot_acf(diff_series)
sm.graphics.tsa.plot_pacf(diff_series)
#arima模型
from statsmodels.tsa.arima_model import ARIMA
model = ARIMA(train_data,order=(p,d,q),freq='')#freq是频率,根据数据填写
arima = model.fit()#训练
print(arima)
pred = arima.predict(start='',end='')#预测

'''