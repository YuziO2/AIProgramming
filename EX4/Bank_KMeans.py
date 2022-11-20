import csv
from math import sqrt
from random import random
from BankDataConvert import Convert


# 从文件中读取数据
def ReadDataSet(filename):
  with open(filename, "rt") as csvfile:
    lines = csv.reader(csvfile, delimiter=';')
    dataSet = list(lines)
    dataSet.pop(0)
    for i in range(len(dataSet)):
      dataSet[i][1] = Convert.Job(dataSet[i][1])
      dataSet[i][2] = Convert.Marital(dataSet[i][2])
      dataSet[i][3] = Convert.Education(dataSet[i][3])
      dataSet[i][4] = Convert.Binary(dataSet[i][4])
      dataSet[i][5] = Convert.Binary(dataSet[i][5])
      dataSet[i][6] = Convert.Binary(dataSet[i][6])
      dataSet[i][7] = Convert.Binary(dataSet[i][7])
      dataSet[i][8] = Convert.Month(dataSet[i][8])
      dataSet[i][9] = Convert.Day(dataSet[i][9])
      dataSet[i][14] = Convert.Binary(dataSet[i][14])
      dataSet[i][20] = Convert.Binary(dataSet[i][20])
      for j in range(len(dataSet[i])):
        dataSet[i][j] = float(dataSet[i][j])
    return dataSet


# 选定质心，并分类
def CalculateCentroid(dataSet, centroid):
  groups = [[], []]
  for i in range(len(dataSet)):
    distances = [[i, 0] for i in range(len(centroid))]  # distance[0]指哪个中心点，distance[1]指距该中心点距离
    for k in range(len(centroid)):
      for j in range(len(dataSet[0])-1):  # 计算欧式距离
        distances[k][1] += pow(dataSet[i][j]-centroid[k][j], 2)
      distances[k][1] = sqrt(distances[k][1])
    distances.sort(key=lambda ele: ele[1])
    groups[distances[0][0]].append(dataSet[i])  # 向相应group放入该实例
  newCentroid = [[0.0 for _ in range(len(dataSet[0]) - 1)] for _ in range(len(centroid))]
  for i in range(len(groups)):  # 0到1
    for k in range(len(dataSet[0])-1):  # 0到19
      for j in range(len(groups[i])):   # 本分类的实例数
        newCentroid[i][k] += groups[i][j][k]
      newCentroid[i][k] /= len(groups[i])  # 通过平均数来求出新的中心点
  return [newCentroid, groups]


if __name__ == "__main__":
  dataSet = ReadDataSet(r'./bank-additional.csv')
  K = 2
  centroid = [dataSet[int(random()*len(dataSet))] for _ in range(K)]
  #print(centroid)
  [newCentroid, groups] = CalculateCentroid(dataSet, centroid)
  while newCentroid != centroid:  # 一直循环，直到所有中心点不再变
    centroid = newCentroid
    [newCentroid, groups] = CalculateCentroid(dataSet, centroid)
  print('在经过KMeans聚类算法后，分组情况如下：\n')
  for i in range(len(groups)):
    result = [0, 0]
    for j in range(len(groups[i])):
      if groups[i][j][20] == 1.0:
        result[0] += 1
      elif groups[i][j][4] == 0.0:
        result[1] += 1
    print('第'+str(i+1)+'组，共'+str(len(groups[i]))+'项，其中y:'+str(result[0])+'项；' +
          'n:'+str(result[1])+'项；')
