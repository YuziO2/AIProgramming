import csv
import math
import random
import numpy as np


# 从文件中读取数据
def ReadDataSet(filename):
  with open(filename, "rt") as csvfile:
    lines = csv.reader(csvfile)
    dataSet = list(lines)
    for x in range(len(dataSet)):
      for y in range(4):
        dataSet[x][y] = float(dataSet[x][y])
  return dataSet


# 拆分数据集
def SplitDataSet(dataSet, PROPORTION, trainSet, testSet):
  for i in range(len(dataSet)):
    if random.random() <= PROPORTION:
      trainSet.append(dataSet[i])
    else:
      testSet.append(dataSet[i])


# 区分类型
def DistinguishTypes(trainSet, type):
  result = []
  for i in range(len(trainSet)):
      if trainSet[i][-1] == type:
          result.append(trainSet[i][0:4])
  return result


# 正态分布
def NormalDistribution(x, η, σ2):
  return (1.0/(math.sqrt(2*math.pi)*math.sqrt(σ2)))*math.exp(-(math.pow((x-η), 2))/(2*σ2))


# 贝叶斯算法
def BayesianAlgorithm(typeSetosa, typeVersicolor, typeVirginica, testSet):
  prediction = []
  setosaMean = np.mean(typeSetosa, axis=0)
  setosaVar = np.var(typeSetosa, axis=0)
  versicolorMean = np.mean(typeVersicolor, axis=0)
  versicolorVar = np.var(typeVersicolor, axis=0)
  virginicaMean = np.mean(typeVirginica, axis=0)
  virginicaVar = np.var(typeVirginica, axis=0)
  for i in range(len(testSet)):
    separate = [[0.0 for col in range(4)] for row in range(3)]  # 创建一个 3行4列 的数组
    separate[0][0] = NormalDistribution(testSet[i][0], setosaMean[0], setosaVar[0])
    separate[0][1] = NormalDistribution(testSet[i][1], setosaMean[1], setosaVar[1])
    separate[0][2] = NormalDistribution(testSet[i][2], setosaMean[2], setosaVar[2])
    separate[0][3] = NormalDistribution(testSet[i][3], setosaMean[3], setosaVar[3])
    separate[1][0] = NormalDistribution(testSet[i][0], versicolorMean[0], versicolorVar[0])
    separate[1][1] = NormalDistribution(testSet[i][1], versicolorMean[1], versicolorVar[1])
    separate[1][2] = NormalDistribution(testSet[i][2], versicolorMean[2], versicolorVar[2])
    separate[1][3] = NormalDistribution(testSet[i][3], versicolorMean[3], versicolorVar[3])
    separate[2][0] = NormalDistribution(testSet[i][0], virginicaMean[0], virginicaVar[0])
    separate[2][1] = NormalDistribution(testSet[i][1], virginicaMean[1], virginicaVar[1])
    separate[2][2] = NormalDistribution(testSet[i][2], virginicaMean[2], virginicaVar[2])
    separate[2][3] = NormalDistribution(testSet[i][3], virginicaMean[3], virginicaVar[3])
    collect = {}
    collect['Iris-setosa'] = separate[0][0]*separate[0][1]*separate[0][2]*separate[0][3]
    collect['Iris-versicolor'] = separate[1][0]*separate[1][1]*separate[1][2]*separate[1][3]
    collect['Iris-virginica'] = separate[2][0]*separate[2][1]*separate[2][2]*separate[2][3]
    prediction.append(sorted(collect.items(), key=lambda kv: (kv[1]), reverse=True)[0][0])
  return prediction

if __name__ == "__main__":
  dataSet = ReadDataSet(r'./iris.data')
  PROPORTION = 0.8  # 训练集比例
  testSet = []
  trainSet = []
  SplitDataSet(dataSet, PROPORTION, trainSet, testSet)
  print("数据集总量为："+str(len(dataSet))+"， 其中训练集数量为：" +
        str(len(trainSet))+"， 测试集数量为："+str(len(testSet)))
  typeSetosa = DistinguishTypes(trainSet, 'Iris-setosa')
  typeVersicolor = DistinguishTypes(trainSet, 'Iris-versicolor')
  typeVirginica = DistinguishTypes(trainSet, 'Iris-virginica')
  prediction = BayesianAlgorithm(typeSetosa, typeVersicolor, typeVirginica, testSet)
  correctNum = 0
  for i in range(len(testSet)):
    # 比较正确率
    if prediction[i] == testSet[i][-1]:
      correctNum += 1
  print("在经过贝叶斯分类后，正确率为："+str(correctNum/len(testSet)))
