import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#参数设置/parameter setting
timesteps = seq_length = 20 #时间窗/window length
data_dim = 5 #输入数据维度/dimension of input data
output_dim = 1 #输出数据维度/dimension of output data

#数据准备/data preparation 
#变量选取Open,High,Low,Close,Volume，以浦发银行股票为例
stock_data = ts.get_k_data('600000',start='2016-01-01',end='2018-11-20')
xy = stock_data[['open','close','high','low','volume']]
xy = np.array(xy.values)

#切分训练集合测试集/split to train and testing
train_size = int(len(xy) * 0.7)
test_size = len(xy) - train_size
xy_train, xy_test = np.array(xy[0:train_size]),np.array(xy[train_size:len(xy)])

#对training set进行预处理
scaler = MinMaxScaler()
xy_train_new = scaler.fit_transform(xy_train)
x_new = xy_train_new[:,0:5]
y_new = xy_train_new[:,1]

x = x_new
y = y_new
dataX = []
dataY = []
for i in range(0, len(y) - seq_length):
    _x = x[i:i + seq_length]
    _y = y[i + seq_length]  # Next close price
    print(_x, "->", _y)
    dataX.append(_x)
    dataY.append(_y)

#处理数据shape,准备进入神经网络层
x_real = np.vstack(dataX).reshape(-1,seq_length,data_dim)
y_real= np.vstack(dataY).reshape(-1,output_dim)
print(x_real.shape)
print(y_real.shape)
dataX = x_real
dataY = y_real

trainX, trainY = dataX, dataY

#对test set进行预处理，这里用了training的scaler
xy_test_new = scaler.transform(xy_test)
x_new = xy_test_new[:,0:5]
y_new = xy_test_new[:,1]

x = x_new
y = y_new
dataX = []
dataY = []
for i in range(0, len(y) - seq_length):
    _x = x[i:i + seq_length]
    _y = y[i + seq_length]  # Next price change
    print(_x, "->", _y)
    dataX.append(_x)
    dataY.append(_y)

#处理数据shape,准备进入神经网络层
x_real = np.vstack(dataX).reshape(-1,seq_length,data_dim)
y_real= np.vstack(dataY).reshape(-1,output_dim)
print(x_real.shape)
print(y_real.shape)
dataX = x_real
dataY = y_real

testX, testY = dataX, dataY

from keras.layers import Input, Dense, LSTM, merge
from keras.models import Model

# 构建神经网络层 1层LSTM层+3层Dense层
lstm_input = Input(shape=(seq_length, data_dim), name='lstm_input')#shape: 形状元组（整型）不包括batch size。表示了预期的输入将是一批（seq_len,data_dim）的向量。
lstm_output = LSTM(128, activation='tanh', dropout=1.0)(lstm_input)#LSTM网络
#units: Positive integer,dimensionality of the output space.
#dropout: Float between 0 and 1. Fraction of the units to drop for the linear transformation of the inputs.
Dense_output_1 = Dense(64, activation='relu')(lstm_output)#全连接网络
Dense_output_2 = Dense(16, activation='relu')(Dense_output_1)#全连接网络
predictions = Dense(output_dim, activation='tanh')(Dense_output_2)#全连接网络

model = Model(inputs=lstm_input, outputs=predictions)
#This model will include all layers required in the computation of output given input.
model.compile(optimizer='adam', loss='mse', metrics=['mse'])
#Configures the model for training.
#optimizer: String (name of optimizer) or optimizer instance. See optimizers.
#loss: String (name of objective function) or objective function.The loss value will be minimized by the model.
#metrics: List of metrics to be evaluated by the model during training and testing. Typically you will use  metrics=['accuracy'].
model.fit(trainX, trainY, batch_size=len(trainX), epochs=100, verbose=2)
#Trains the model for a given number of epochs (iterations on a dataset).
#verbose: Integer. 0, 1, or 2. Verbosity mode. 0 = silent, 1 = progress bar, 2 = one line per epoch.

# 保存模型
model.save('model.h5')   # HDF5文件，pip install h5py

trainPredict = model.predict(trainX)
trainPredict1 = trainPredict * scaler.data_range_[1] + scaler.data_min_[1]
trainY1 = trainY * scaler.data_range_[1] + scaler.data_min_[1]
plt.plot(trainY1,color='blue')
plt.plot(trainPredict1,color='orange')
plt.show()
print(max(abs(trainPredict1 - trainY1)))

# 载入模型
from keras.models import load_model
model = load_model('model.h5')

testPredict = model.predict(testX)
testPredict1 = testPredict * scaler.data_range_[1] + scaler.data_min_[1]
testY1 = testY * scaler.data_range_[1] + scaler.data_min_[1]
plt.plot(testY1,color='blue')
plt.plot(testPredict1,color='orange')
plt.show()
print(max(abs(testPredict1 - testY1)))
