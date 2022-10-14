import csv
import math
import random
import numpy as np


# 从文件中读取数据
def ReadDataSet(filename):
  with open(filename, "rt") as csvfile:
    lines = csv.reader(csvfile, delimiter=';')
    dataSet = list(lines)
    dataSet.pop(0)
    numFeatures = [0, 10, 11, 12, 13, 15, 16, 17, 18, 19]
    for i in range(len(dataSet)):
      for j in numFeatures:
        dataSet[i][j] = float(dataSet[i][j])
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
          result.append(trainSet[i][0:21])
  return result


# 正态分布
def NormalDistribution(x, η, σ2):
  return (1.0/(math.sqrt(2*math.pi)*math.sqrt(σ2)))*math.exp(-(math.pow((x-η), 2))/(2*σ2))


# 贝叶斯算法
def BayesianAlgorithm(typeYes, typeNo, testSet):
  prediction = []

  def yesMean(column):
    return np.mean([float(i) for i in np.array(typeYes)[:, column]])

  def yesVar(column):
    return np.var([float(i) for i in np.array(typeYes)[:, column]])

  def noMean(column):
    return np.mean([float(i) for i in np.array(typeNo)[:, column]])

  def noVar(column):
    return np.var([float(i) for i in np.array(typeNo)[:, column]])

  # 计算非数字属性，使用贝叶斯定理
  def NumOfFeatureBelongsToType(feature, column, type):
    result = 0
    for i in range(len(type)):
      if type[i][column] == feature:
        result += 1
    return result
  strDictionary = {}
  strFeatures = {}
  strFeatures['job'] = {'value': ['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management',
                        'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'unknown'], 'column': 1}
  strFeatures['marital'] = {'value': ['single', 'married', 'divorced', 'unknown'], 'column': 2}
  strFeatures['education'] = {'value': ['illiterate', 'basic.4y', 'basic.6y', 'basic.9y',
                                        'high.school', 'university.degree', 'professional.course', 'unknown'], 'column': 3}
  strFeatures['default'] = {'value': ['no', 'yes', 'unknown'], 'column': 4}
  strFeatures['housing'] = {'value': ['no', 'yes', 'unknown'], 'column': 5}
  strFeatures['loan'] = {'value': ['no', 'yes', 'unknown'], 'column': 6}
  strFeatures['contact'] = {'value': ['cellular', 'telephone'], 'column': 7}
  strFeatures['month'] = {'value': ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], 'column': 8}
  strFeatures['day'] = {'value': ['mon', 'tue', 'wed', 'thu', 'fri'], 'column': 9}
  strFeatures['poutcome'] = {'value': ['failure', 'success', 'nonexistent'], 'column': 14}
  for feature in strFeatures.items():
    for option in feature[1]['value']:
      Yes = NumOfFeatureBelongsToType(option, feature[1]['column'], typeYes)
      No = NumOfFeatureBelongsToType(option, feature[1]['column'], typeNo)
      strDictionary[feature[0]+'|'+option+'|yes'] = Yes/len(typeYes)
      strDictionary[feature[0]+'|'+option+'|no'] = No/len(typeNo)
      strDictionary[feature[0]+'|'+option] = (Yes+No)/(len(typeYes)+len(typeNo))

  for i in range(len(testSet)):
    collect = {}
    collect['yes'] = 1.0
    numFeatures = [0, 10, 11, 12, 13, 15, 16, 17, 18, 19]
    for column in numFeatures:
      collect['yes'] *= NormalDistribution(testSet[i][column], yesMean(column), yesVar(column))
    strNumerator = 1.0
    strDenominator = 1.0
    for feature in strFeatures.items():
      strNumerator *= strDictionary[feature[0]+'|'+testSet[i][feature[1]['column']]+'|yes']
      strDenominator *= strDictionary[feature[0]+'|'+testSet[i][feature[1]['column']]]
    collect['yes'] *= strNumerator/strDenominator

    collect['no'] = 1.0
    numFeatures = [0, 10, 11, 12, 13, 15, 16, 17, 18, 19]
    for column in numFeatures:
      collect['no'] *= NormalDistribution(testSet[i][column], noMean(column), noVar(column))
    strNumerator = 1.0
    strDenominator = 1.0
    for feature in strFeatures.items():
      strNumerator *= strDictionary[feature[0]+'|'+testSet[i][feature[1]['column']]+'|no']
      strDenominator *= strDictionary[feature[0]+'|'+testSet[i][feature[1]['column']]]
    collect['no'] *= strNumerator/strDenominator
    if (collect['yes'] >= collect['no']):
      prediction.append('yes')
    else:
      prediction.append('no')
    if (i % 10 == 0):
      print('完成'+str(i+1)+'项了！')
  return prediction


if __name__ == "__main__":
  dataSet = ReadDataSet(r'./bank-additional.csv')
  PROPORTION = 0.8  # 训练集比例
  testSet = []
  trainSet = []
  SplitDataSet(dataSet, PROPORTION, trainSet, testSet)
  print("数据集总量为："+str(len(dataSet))+"， 其中训练集数量为：" +
        str(len(trainSet))+"， 测试集数量为："+str(len(testSet)))
  typeYes = DistinguishTypes(trainSet, 'yes')
  typeNo = DistinguishTypes(trainSet, 'no')
  prediction = BayesianAlgorithm(typeYes, typeNo, testSet)
  correctNum = 0
  for i in range(len(testSet)):
    # 比较正确率
    if prediction[i] == testSet[i][-1]:
      correctNum += 1
  print("在经过贝叶斯分类后，正确率为："+str(correctNum/len(testSet)))
