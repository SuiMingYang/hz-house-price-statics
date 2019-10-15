from xgboost import XGBClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
 
# load data from CSV file,
def loadData(fileFullPath):
    if (fileFullPath == None):
        print('file path is empty, please check path!')
    # use pandas read CSV file, return DataFrame
    dataSet = pd.read_csv(fileFullPath)
    pd.set_option('display.max_columns',20)
    # split features and labels
    featureNum = dataSet.shape[1]
    trainData = dataSet.iloc[:,0:featureNum-1]
    trainLabel = dataSet.iloc[:,-1]
    return trainData, trainLabel


def XGBDemo1(trainData, trainLabel):
    if (trainData.empty or trainLabel.empty):
        print('data is empty. please check data!')
        return
    # split train set,
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(trainData, trainLabel, test_size=0.3, random_state=0)
    # build XGBoost model
    model = XGBClassifier(n_jobs=-1)
    # train model by train data
    model.fit(Xtrain, Ytrain)
    # test model by test data
    Ypred = model.predict(Xtest)
    # compute the accuracy of model
    accuracy = accuracy_score(Ytest, Ypred)
    print(accuracy)

# Use GridSearchCV find XGBoost best param
def XGBDemo2(trainData, trainLabel):
    if (trainData.empty or trainLabel.empty):
        print('data is empty. please check data!')
        return
    #split train data and test data
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(trainData, trainLabel, test_size=0.3, random_state=0)
    print('train size:',Xtrain.shape)
    # construct params grid
    learningRate = [0.0001, 0.0003, 0.0002, 0.0005, 0.0007, 0.001, 0.01, 0.1, 0.2, 0.3]
    maxDepth = [1, 2, 3, 4, 5]
    parammGrid = dict(learningRate = learningRate, maxDepth = maxDepth)
    # Stratified K fold
    kfold = StratifiedKFold(n_splits=10, random_state=0, shuffle=True)
    # define model
    model = XGBClassifier()
    # use grid search cross validation search best param
    gridSearch = GridSearchCV(model,param_grid=parammGrid,scoring='neg_log_loss',n_jobs=-1,cv=kfold)
    gridFit = gridSearch.fit(Xtrain,Ytrain)
    Ypred = gridFit.predict(Xtest)
    accScore = accuracy_score(Ytest,Ypred)
    print('find best para, para :',gridFit.best_params_,', best score:',gridFit.best_score_,', accuracy:',accScore)

if __name__ == '__main__':
    fileFullPath = './data_history/houseinfo.csv'
    trainData, trainLabel = loadData(fileFullPath)
    XGBDemo1(trainData, trainLabel)
    XGBDemo2(trainData, trainLabel)



