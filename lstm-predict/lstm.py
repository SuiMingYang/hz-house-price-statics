import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Activation

def load_data(file_name, sequence_length=10, split=0.8):
    # 提取数据一列
    df = pd.read_csv(file_name)['']
    # 把数据转换为数组
    data_all = np.array(df).astype(float)
    # 将数据缩放至给定的最小值与最大值之间，这里是０与１之间，数据预处理
    scaler = MinMaxScaler()
    data_all = scaler.fit_transform(data_all)
    print(len(data_all))   
    data = []
    # 构造送入lstm的3D数据：(133, 11, 1)
    for i in range(len(data_all) - sequence_length - 1):
        data.append(data_all[i: i + sequence_length + 1])
    reshaped_data = np.array(data).astype('float64')
    print(reshaped_data.shape)
    # 打乱第一维的数据
    np.random.shuffle(reshaped_data)
    print('reshaped_data:',reshaped_data[0])
    # 这里对133组数据进行处理，每组11个数据中的前10个作为样本集：(133, 10, 1)
    x = reshaped_data[:, :-1]
    print('samples:',x.shape)
    # 133组样本中的每11个数据中的第11个作为样本标签
    y = reshaped_data[:, -1]
    print('labels:',y.shape)
    # 构建训练集(训练集占了80%)
    split_boundary = int(reshaped_data.shape[0] * split)
    train_x = x[: split_boundary]
    # 构建测试集(原数据的后20%)
    test_x = x[split_boundary:]
    # 训练集标签
    train_y = y[: split_boundary]
    # 测试集标签
    test_y = y[split_boundary:]
    # 返回处理好的数据
    return train_x, train_y, test_x, test_y, scaler

# 模型建立
def build_model():
    # input_dim是输入的train_x的最后一个维度，train_x的维度为(n_samples, time_steps, input_dim)
    model = Sequential()
    model.add(LSTM(100,return_sequences=True))
    print(model.layers)
    model.add(LSTM(100, return_sequences=False))
    model.add(Dense(1))
    model.add(Activation('linear'))

    model.compile(loss='mse', optimizer='rmsprop')
    return model


def train_model(train_x, train_y, test_x, test_y,scaler):
    model = build_model()
    val_x=scaler.transform([[500],[354],[645],[789],[879],[456],[745],[600],[800],[900]])
    try:
        model.fit(train_x, train_y, batch_size=512, nb_epoch=30, validation_split=0.1)
        predict = model.predict(test_x)
        val_y=model.predict(np.array([val_x]))
        predict = np.reshape(predict, (predict.size, ))
    except KeyboardInterrupt:
        print(predict)
        print(test_y)
    print('predict:\n',predict)
    print('test_y:\n',test_y)
    # 预测的散点值和真实的散点值画图
    try:
        fig1 = plt.figure(1)
        plt.plot(predict, 'r:')
        plt.plot(test_y, 'g-')
        plt.legend(['predict', 'true'])
    except Exception as e:
        print(e)
    return predict, test_y


if __name__ == '__main__':
    # 加载数据
    train_x, train_y, test_x, test_y, scaler = load_data('./house_score.csv')    
    train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1], 1))
    test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1], 1))
    # 模型训练  
    
    predict_y, test_y = train_model(train_x, train_y, test_x, test_y,scaler)
    # 对标准化处理后的数据还原
    predict_y = scaler.inverse_transform([[i] for i in predict_y])
    test_y = scaler.inverse_transform(test_y)
    # 把预测和真实数据对比
    fig2 = plt.figure(2)
    plt.plot(predict_y, 'g:')
    plt.plot(test_y, 'r-')
    plt.legend(['predict', 'true'])
    plt.show()
