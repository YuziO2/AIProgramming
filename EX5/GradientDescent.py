import csv
from random import random
import matplotlib.pyplot as plt
import numpy


# 从文件中读取数据
def ReadDataSet(filename):
  with open(filename, "rt") as csvfile:
    lines = list(csv.reader(csvfile))
    lines.pop(0)
    dataSet = [[] for _ in range(2)]
    for x in range(len(lines)):
      if random() < 0.1:
        dataSet[0].append(float(lines[x][7]))
        dataSet[1].append(float(lines[x][8]))
  return dataSet


# y = b + mx
def ComputeError(b, m, points):
    totalError = sum((((b + m * point[0]) - point[1]) ** 2 for point in points))
    return totalError / float(len(points))


def step_gradient(b_current, m_current, points, learningRate):
    b_gradient = 0
    m_gradient = 0
    N = float(len(points))
    for i in range(0, len(points)):
        x = points[i, 0]
        y = points[i, 1]
        m_gradient += (1 / N) * x * ((b_current + m_current * x) - y)
        b_gradient += (1 / N) * ((b_current + m_current * x) - y)
    new_b = b_current - (learningRate * b_gradient)  # 沿梯度负方向
    new_m = m_current - (learningRate * m_gradient)  # 沿梯度负方向
    return [new_b, new_m]


if __name__ == "__main__":
  dataSet = ReadDataSet(r'./housing_mini.csv')
  #print(dataSet[1])
  points = numpy.array([[dataSet[0][i], dataSet[1][i]]for i in range(len(dataSet[0]))])
  b = 0.0
  m = 0.0
  for i in range(1000):
    [b, m] = step_gradient(b, m, points, 0.001)
    print(b, m)
  plt.scatter(dataSet[0], dataSet[1], 5)
  plt.plot([1, 10], [b+m, b+10*m], 'red')
  plt.show()
