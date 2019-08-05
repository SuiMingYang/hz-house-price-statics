# -*- coding: utf-8 -*-
"""
https://www.evolutionarylearn.com/paper/python-keras-tensorflow-mts/#comment-48
"""

import time
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras import backend as K  # Keras解决OOM超内存问题

"""
预测房价
"""

np.random.seed(1)  # Fix random seed for reproducibility/设定随机种子，保证实验可复现

class lstm():

    def __init__(self, dataset, hyper_params):
        self.dataset = dataset  # Initialize data sets/数据集初始化
        self.num_neur = hyper_params[0]  # Initialize number of layer and number of neurons in each layer/初始化隐层数和各层神经元个数
        self.look_back = hyper_params[1]  # Initialize length of windows/初始化窗口长度
        self.epochs = hyper_params[2]  # Initialize training times/初始化训练次数
        self.batch_size = hyper_params[3]  # Initialize batch size/初始化批数
        self.selected_feature = hyper_params[4]  # Initialize the selected features/初始化选择特征
        self.train_ratio = hyper_params[5]  # Initialize the splitted ratio of training/初始化训练集分割比例
        self.feature_num = hyper_params[6]  # Initialize the number of features/初始化特征数量
        self.x_train = []  # Initialize training features of training data set/初始化训练集x部分-训练特征
        self.y_train = []  # Initialize supervisory signals of training data set/初始化训练集y部分-监督信号
        self.x_test = []  # Initialize test features of training data set/初始化测试集x部分-测试特征
        self.y_test = []  # Initialize supervisory signals of training data set/初始化测试集y部分-监督信号

    # Split into train and test sets/分割训练集与测试集
    def split_dataset(self):
        # Feature selection/特征选择
        def feature_selection(selected_feature):
            selected_list = []
            for index, item in enumerate(selected_feature):
                if item == 1:
                    selected_list.append(index)
                else:
                    if index == 1:
                        selected_list.append(index)
            return selected_list

        # Convert an array of values into a dataset matrix/转换数据结构，准备训练集与测试集
        def create_dataset(dataset, look_back):
            dataX, dataY = [], []
            for i in range(len(dataset) - look_back):
                a = dataset[i:(i + look_back), 0:dataset.shape[1]]
                dataX.append(a)
                dataY.append(dataset[i + look_back, 0])
            return np.array(dataX), np.array(dataY)

        selected_list = feature_selection(self.selected_feature)  # Index list of selected feature/选择特征列表索引
        train_size = int(len(self.dataset) * self.train_ratio)  # Size of training data set/训练集大小
        train_data = self.dataset[0:train_size, selected_list]  # Training data set/训练集
        test_data = self.dataset[train_size - self.look_back - 1:len(self.dataset), selected_list]  # Test data set/测试集
        self.feature_num = len(selected_list)  # Update the number of selected feature/更新特征数量

        # Data set detail/具体分割后数据集
        x_train, self.y_train = create_dataset(train_data, self.look_back)
        x_test, self.y_test = create_dataset(test_data, self.look_back)

        # Reshape input to be [samples, feature_num, features]/整理特征数据的格式
        self.x_train = np.reshape(x_train, (x_train.shape[0], self.feature_num, x_train.shape[1]))
        self.x_test = np.reshape(x_test, (x_test.shape[0], self.feature_num, x_test.shape[1]))

    # Create and fit the LSTM network/创建并拟合LSTM网络
    def lstm(self):
        start_cr_a_fit_net = time.time()  # Record time/记录网络创建与训练时间
        self.split_dataset()  # Split the data set/数据分割

        # Create and fit the LSTM network/创建并拟合LSTM网络
        LSTM_model = Sequential()
        for i in range(len(self.num_neur)):  # 构建多层网络
            if len(self.num_neur) == 1:
                LSTM_model.add(LSTM(self.num_neur[i], input_shape=(None, self.look_back)))
            else:
                if i < len(self.num_neur) - 1:
                    LSTM_model.add(LSTM(self.num_neur[i], input_shape=(None, self.look_back), return_sequences=True))
                else:
                    LSTM_model.add(LSTM(self.num_neur[i], input_shape=(None, self.look_back)))

        LSTM_model.add(Dense(1))
        LSTM_model.summary()  # Summary the structure of neural network/网络结构总结
        LSTM_model.compile(loss='mean_squared_error', optimizer='adam')  # Compile the neural network/编译网络
        LSTM_model.fit(self.x_train, self.y_train, epochs=self.epochs, batch_size=self.batch_size
                       , verbose=0)  # Fit the LSTM network/拟合LSTM网络
        end_cr_a_fit_net = time.time() - start_cr_a_fit_net
        print('Running time of creating and fitting the LSTM network: %.2f Seconds' % (end_cr_a_fit_net))

        # LSTM prediction/LSTM进行预测
        trainPredict = LSTM_model.predict(self.x_train)  # Predict by training data set/训练集预测
        testPredict = LSTM_model.predict(self.x_test)  # Predict by test data set/测试集预测
        return LSTM_model,trainPredict, testPredict, self.y_train, self.y_test

    # Evaluate network performance/评估网络效果
    def mape(self, scaler, trainPredict, testPredict):
        # Invert predictions start / 将预测值转换为正常数值
        # Create empty table like the dataset/创建一个空的数组, 结构同dataset
        trainPredict_dataset_like = np.zeros(shape=(len(trainPredict), self.dataset.shape[1]))
        # Put the predicted values in the right field/将预测值填充进新建数组
        trainPredict_dataset_like[:, 0] = trainPredict[:, 0]
        # Inverse transform and then select the right field/数据转换
        trainPredict = scaler.inverse_transform(trainPredict_dataset_like)[:, 0]

        y_train_dataset_like = np.zeros(shape=(len(self.y_train), self.dataset.shape[1]))
        y_train_dataset_like[:, 0] = self.y_train
        self.y_train = scaler.inverse_transform(y_train_dataset_like)[:, 0]

        testPredict_dataset_like = np.zeros(shape=(len(testPredict), self.dataset.shape[1]))
        testPredict_dataset_like[:, 0] = testPredict[:, 0]
        testPredict = scaler.inverse_transform(testPredict_dataset_like)[:, 0]

        y_test_dataset_like = np.zeros(shape=(len(self.y_test), self.dataset.shape[1]))
        y_test_dataset_like[:, 0] = self.y_test
        self.y_test = scaler.inverse_transform(y_test_dataset_like)[:, 0]
        # Invert predictions end/数据转换结束

        # Calculate root mean squared error and MAPE/计算RMSE和误差率MAPE
        train_RMSE = math.sqrt(mean_squared_error(self.y_train, trainPredict))
        test_RMSE = math.sqrt(mean_squared_error(self.y_test, testPredict))
        trainMAPE = np.mean(np.abs(self.y_train - trainPredict) / self.y_train)
        testMAPE = np.mean(np.abs(self.y_test - testPredict) / self.y_test)

        print("Train RMSE: " + str(round(train_RMSE, 2)) + '  ' + "Train MAPE: " + str(round(trainMAPE * 100, 2)))
        print("Test RMSE: " + str(round(test_RMSE, 2)) + '  ' + "Test MAPE: " + str(round(testMAPE * 100, 2)))
        return trainMAPE, testMAPE, trainPredict, testPredict

    # Visualization results/可视化结果
    def plot(self, scaler, trainPredict, testPredict):
        # Shift training predictions for plotting/转换数据结构用于作图-训练预测结果
        sub_traindataset = [[data] for data in self.dataset[:, 0]]
        trainPredictPlot = np.empty_like(sub_traindataset)
        trainPredictPlot[:, 0] = np.nan
        trainPredictPlot[self.look_back:len(trainPredict) + self.look_back, 0] = trainPredict

        # Shift test predictions for plotting/转换数据结构用于作图-测试预测结果
        sub_testdataset = [[data] for data in self.dataset[:, 0]]
        testPredictPlot = np.empty_like(sub_testdataset)
        testPredictPlot[:] = np.nan
        testPredictPlot[len(trainPredict) + self.look_back - 1:len(self.dataset), 0] = testPredict

        # plot baseline and predictions/作图
        datasety_like = np.zeros(shape=(self.dataset.shape[0], self.dataset.shape[1]))
        datasety_like[:, 0] = self.dataset[:, 0]
        y = scaler.inverse_transform(datasety_like)[:, 0]

        dates = pd.date_range('2010-12', periods=len(y), freq='M')
        xs = [datetime.strptime(str(d)[0:7], '%Y-%m').date() for d in dates]
        # 配置横坐标
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))

        A, = plt.plot(xs, y[0:len(y)], linewidth='2', color='r')  # 真实值
        B, = plt.plot(xs, trainPredictPlot, linewidth='1.5', color='g')  # LSTM训练集结果
        C, = plt.plot(xs, testPredictPlot, linewidth='4', color='g')  # LSTM测试集结果

        # plt.plot(NpredYPlot,linewidth = '3',color='k')
        plt.axvline(xs[76], linewidth='2', color='black')  # 画直线区分训练部分与测试部分
        plt.legend((A, B, C), ('real_value', 'LSTM_train', 'LSTM_test'), loc='best')
        plt.gcf().autofmt_xdate()  # 自动旋转日期标记

        plt.xlabel('Date', family='Times New Roman', fontsize=16)  # X轴
        plt.ylabel('Housing price', family='Times New Roman', fontsize=16)  # Y轴

        plt.title('LSTM', family='Times New Roman', fontsize=16)  # 添加标题

        plt.savefig(r'result.png', dpi=900)  # 保存图片

        plt.show()
        del trainPredictPlot, testPredictPlot


if __name__ == "__main__":
    # Load the dataset/导入数据集
    file = r'./lstm-predict/data.xlsx'
    dataframe = pd.read_excel(file, sheet_name=0, header=0, index_col=None)
    dataset = dataframe.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8]].values
    dataset = dataset.astype('float32')

    # Normalize the dataset/标准化数据集
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)

    # Set hyper-parameters/设定超参数
    num_neur = [15, 10]  # Number of layer and number of neurons in each layer/隐藏层数和各层神经元个数
    look_back = 1  # Length of windows/窗口长度
    epochs = 100  # Training times/训练次数
    batch_size = 10 # Batch size/批数大小
    select_feature = [1, 1, 1, 0, 0, 0, 1, 0]  # Selected features list/被选择特征列表
    train_ratio = 0.85  # Splitted ratio of training data set/训练集分割比例
    feature_num = dataset.shape[1]  # Feature number+y/特征数量+1,也将预测项作为特征
    # Hyper-parameter list/超参数列表
    hyper_params = [num_neur, look_back, epochs, batch_size, select_feature, train_ratio, feature_num]

    # Start an LSTM model/开始一个LSTM网络
    model = lstm(dataset, hyper_params)  # Create instance of LSTM/实例化模型
    api,trainPredict, testPredict, y_train, y_test = model.lstm()  # Create and fit the LSTM network/创建并拟合LSTM网络
    #print(api)


    print(scaler.inverse_transform(api.predict(np.array([scaler.fit_transform([[97.8],[-0.221],[4.9],[68.96]]),scaler.fit_transform([[97.8],[-0.221],[4.9],[68.96]])]))))  # 
    a=[]
    df=dataframe.values
    for i,item in enumerate(dataframe.values): 
        a.append(scaler.fit_transform([[item[1]],[item[2]],[item[3]],[item[7]]])) 
    a.append(scaler.fit_transform([[df[90][1]],[df[90][2]],[df[90][3]],[df[90][7]]]))
    print(scaler.inverse_transform(api.predict(np.array(a)))) 



    trainMAPE, testMAPE, trainPredict, testPredict = model.mape(scaler, trainPredict
                                                                , testPredict)  # Evaluate network performance/评估网络效果
    model.plot(scaler, trainPredict, testPredict)  # Visualization results/可视化结果
    K.clear_session()  # 关掉内存中神经网络
