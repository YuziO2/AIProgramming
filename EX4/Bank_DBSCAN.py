import csv
from random import randint
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
    randNum = randint(0, len(cores)-1)
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
  dataSet = ReadDataSet(r'./bank-additional.csv')
  K = 2  # 簇类数量为2
  C = DBSCAN(dataSet, 120, 4)
  for i in range(1, len(C)+1):
    y = 0
    n = 0
    for j in range(len(C[i])):
      if dataSet[C[i][j]][20] == 1.0:
        y += 1
      else:
        n += 1
    print('第'+str(i)+'组，共'+str(len(C[i]))+'项，其中y: '+str(y) +
          '项；n:'+str(n)+'项')
