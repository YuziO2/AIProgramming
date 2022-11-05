import csv
from math import sqrt
from random import randint, random


# 从文件中读取数据
def ReadDataSet(filename):
  with open(filename, "rt") as csvfile:
    lines = csv.reader(csvfile)
    dataSet = list(lines)
    for x in range(len(dataSet)):
      for y in range(4):
        dataSet[x][y] = float(dataSet[x][y])
  return dataSet


# 计算两个点的欧氏距离
def CalculateDistance(point1, point2):
  result = 0
  for i in range(len(point1)-1):
    result += (point1[i] - point2[i])**2
  return result**0.5


#获取一个点的ε-邻域（记录的是索引）
def getNeighbor(data, dataSet, ε):
  res = []
  for i in range(len(dataSet)):
    if CalculateDistance(data, dataSet[i]) < ε:
      res.append(i)
  return res


def DBSCAN(dataSet, ε, minPoints):
  coreObjs = {}
  C = {}
  for i in range(len(dataSet)):
    neighbor = getNeighbor(dataSet[i], dataSet, ε)
    if len(neighbor) > minPoints:
      coreObjs[i] = neighbor
  oldCoreObjs = coreObjs.copy()
  k = 0
  notAccess = list(range(len(dataSet)))  # 初始化未访问样本集合（索引）
  while len(coreObjs) > 0:
    OldNotAccess = []
    OldNotAccess.extend(notAccess)
    cores = coreObjs.keys()
    #随机选取一个核心对象
    randNum = randint(0, len(cores))
    cores = list(cores)
    core = cores[randNum]
    queue = []
    queue.append(core)
    notAccess.remove(core)
    while len(queue) > 0:
        q = queue[0]
        del queue[0]
        if q in oldCoreObjs.keys():
            delete = [val for val in oldCoreObjs[q] if val in notAccess]  # Δ = N(q)∩Γ
            queue.extend(delete)  # 将Δ中的样本加入队列Q
            notAccess = [val for val in notAccess if val not in delete]  # Γ = Γ\Δ
    k += 1
    C[k] = [val for val in OldNotAccess if val not in notAccess]
    for x in C[k]:
        if x in coreObjs.keys():
            del coreObjs[x]
  return C


if __name__ == "__main__":
  dataSet = ReadDataSet(r'./iris.data')
  K = 3  # 簇类数量为3
  C = DBSCAN(dataSet, 0.4, 2)
  for i in range(1, len(C)+1):
    setosa = 0
    versicolor = 0
    virginica = 0
    for j in range(len(C[i])):
      if C[i][j] < 50:
        setosa += 1
      elif C[i][j] >= 100:
        virginica += 1
      else:
        versicolor += 1
    print('第'+str(i)+'组，共'+str(len(C[i]))+'项，其中Iris-setosa: '+str(setosa) +
          '项；Iris-versicolor:'+str(versicolor)+'项；Iris-virginica:'+str(virginica)+'项')
