import csv
from math import sqrt
import random


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


# 通过邻居来判定测试集的实例从属
def ClassificationByNeighbors(trainSet, instance, K):
  distances = []
  for i in range(len(trainSet)):
    distance = 0
    for j in range(len(instance)-1):  # 计算欧式距离
      distance += pow(trainSet[i][j]-instance[j], 2)
    distance = sqrt(distance)
    distances.append((trainSet[i], distance))
  distances.sort(key=lambda ele: ele[1])
  # 判定从属
  dict = {}
  for i in range(K):  # 邻居即前K个
    if distances[i][0][-1] in dict:
      dict[distances[i][0][-1]] += 1
    else:
      dict[distances[i][0][-1]] = 1
  dict_sorted = sorted(dict.items(), key=lambda ele: ele[1])
  return dict_sorted[0][0]


if __name__ == "__main__":
  dataSet = ReadDataSet(r'./iris.data')
  PROPORTION = 0.8  # 训练集比例
  testSet = []
  trainSet = []
  SplitDataSet(dataSet, PROPORTION, trainSet, testSet)
  print("数据集总量为："+str(len(dataSet))+"， 其中训练集数量为：" +
        str(len(trainSet))+"， 测试集数量为："+str(len(testSet)))
  K = 6
  correctNum = 0
  for i in range(len(testSet)):
    result = ClassificationByNeighbors(trainSet, testSet[i], K)
    # 比较正确率
    if result == testSet[i][-1]:
      correctNum += 1
  print("在K为"+str(K)+"的情况下，经KNN分类后，正确率为："+str(correctNum/len(testSet)))
