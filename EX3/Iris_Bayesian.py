import csv
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


if __name__ == "__main__":
  dataSet = ReadDataSet(r'./iris.data')
  PROPORTION = 0.8  # 训练集比例
  testSet = []
  trainSet = []
  SplitDataSet(dataSet, PROPORTION, trainSet, testSet)
  print("数据集总量为："+str(len(dataSet))+"， 其中训练集数量为：" +
        str(len(trainSet))+"， 测试集数量为："+str(len(testSet)))
