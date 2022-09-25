<script setup>
import { reactive, ref, onMounted } from "vue";
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import Canvas from "./components/Canvas.vue";
const canvas = ref()

const pointsNumber = 10; //城市数量
const points = []; //城市
const distances = []; //距离矩阵
const groupsNumber = 100; //种群数量
const groups = []; //种群
const iterationTimes = 1000; //迭代次数
const crossRate = 0.9; //交叉率
const mutationRate = 0.1; //变异率
//路线类，route:Array;fitness,surviveProbability,distances:Number
function Route(route) {
  this.route = route;
  this.fitness = 0;
  this.surviveProbability = 0;
  this.distance = 0;
}

//画布大小
const width = 1000;
const height = 500;
//初始化城市
for (let i = 0; i < pointsNumber; i++) {
  points.push([
    Math.floor(
      30 + ((Math.random() * 10000) % (width * devicePixelRatio - 60))
    ),
    Math.floor(
      30 + ((Math.random() * 10000) % (height * devicePixelRatio - 60))
    ),
    "#" +
    Math.floor(Math.random() * 0xffffff)
      .toString(16)
      .padStart(6, "0"), //随机颜色
  ]);
}
//计算距离矩阵
for (let i = 0; i < pointsNumber; i++) {
  for (let j = 0; j < pointsNumber; j++) {
    if (!distances[i]) distances[i] = new Array();
    distances[i].push(
      Math.floor(
        Math.sqrt(
          (points[i][0] - points[j][0]) ** 2 +
          (points[i][1] - points[j][1]) ** 2
        )
      )
    );
  }
}
//初始化种群
for (let i = 0; i < groupsNumber; i++) {
  const random = new Array(pointsNumber).fill(0).map((v, i) => i);
  random.sort(() => 0.5 - Math.random());
  groups.push(new Route(random));
}
//计算初始种群中每个个体的适应度及生存概率
//适应度为序列中相邻两城之间的距离之和的倒数
function calculateGroup() {
  let totalFitness = 0;
  for (let i = 0; i < groupsNumber; i++) {
    let totalDistance = 0;
    for (let j = 0; j < pointsNumber - 1; j++)
      totalDistance += distances[groups[i].route[j]][groups[i].route[j + 1]];
    groups[i].distance = totalDistance;
    groups[i].fitness = 1 / totalDistance; //个体的适应度为其总距离的倒数
    totalFitness += groups[i].fitness;
  }
  //计算每个个体的生存概率（被选择概率）,为个体适应度 / 总适应度
  for (let i = 0; i < groupsNumber; i++)
    groups[i].surviveProbability = groups[i].fitness / totalFitness;
}
calculateGroup();

//对生成的groups进行排序
groups.sort((a, b) => b.surviveProbability - a.surviveProbability);
const firstRoute = ref(groups[0].route); //并传给canvas进行绘制

const buttonMessage = ref("开始计算");
function calculate() {
  buttonDisabled.value = true;
  buttonMessage.value = "计算中，请稍后……"
  for (let i = 0; i < iterationTimes; i++) {
    //计算适应度以及生存概率
    calculateGroup();
    //选择开始
    //计算累计的概率
    const totalProbability = new Array(groupsNumber);
    totalProbability[0] = groups[0].surviveProbability;
    for (let j = 1; j < groupsNumber; j++) {
      totalProbability[j] =
        totalProbability[j - 1] + groups[j].surviveProbability;
    }
    //记录被选择的个体，利用赌轮选择法，随机生成0~1之间一个数，根据计算出来的累计概率选择个体
    let selectedGroups = new Array(groupsNumber);
    for (let j = 0; j < groupsNumber; j++) {
      for (let k = 0; k < groupsNumber; k++) {
        if (Math.random() <= totalProbability[k]) {
          selectedGroups[j] = groups[k];
          break;
        }
      }
    }
    //被选择的种群覆盖初始种群
    for (let j = 0; j < groupsNumber; j++) {
      groups[j] = selectedGroups[j];
    }
    //选择结束，交叉开始
    //第k（k=0、2、4、...、2n）个个体和k+1个个体有一定的概率交叉变换
    //设置一个0~1之间的随机数，若在Pc（交配率）范围内，则该该个体k与下一个个体k+1进行交配
    //随机生成子代交配时DNA交换的数量(1~pointsNumber / 2)
    let changeNumber = Math.floor(
      ((Math.random() * pointsNumber * 10) % (pointsNumber / 2)) + 1
    );
    //交叉
    for (let j = 0; j < groupsNumber - 1; j += 2) {
      //在交叉率以内，则该个体i与下一个个体i+1进行交叉
      if (Math.random() < crossRate) {
        let changePoint = Math.floor((Math.random() * pointsNumber * 10) % (pointsNumber - changeNumber))  //交叉点
        let map = new Map()
        for (let k = changePoint; k < changeNumber + changePoint; k++) {//建立不重复的映射
          let temp1 = groups[j].route[k]
          let temp2 = groups[j + 1].route[k]
          groups[j].route[k] = temp2
          groups[j + 1].route[k] = temp1//交换
          if (map.has(temp1)) {
            temp1 = map.get(temp1)
          }
          if (map.has(temp2)) {
            temp2 = map.get(temp2)
          }
          map.set(temp1, temp2)
          map.set(temp2, temp1)
        }
        //利用映射解决基因冲突问题
        for (let k = 0; k < pointsNumber; k++) {
          if (k >= changePoint && k < changeNumber + changePoint)
            continue
          if (map.has(groups[j].route[k]))
            groups[j].route[k] = map.get(groups[j].route[k])
          if (map.has(groups[j + 1].route[k]))
            groups[j + 1].route[k] = map.get(groups[j + 1].route[k])
        }
      }
    }
    //变异
    //每个实例都有可能基因（路径）多次变换
    for (let j = 0; j < groupsNumber; j++) {
      if (Math.random() < mutationRate) {
        for (let exchangeTime = Math.floor(Math.random() * pointsNumber + 1); exchangeTime > 0; exchangeTime--) {
          const changePointA = Math.floor(Math.random() * pointsNumber)
          const changePointB = Math.floor(Math.random() * pointsNumber)
          const temp = groups[j].route[changePointA]
          groups[j].route[changePointA] = groups[j].route[changePointB]
          groups[j].route[changePointB] = temp
        }
      }
    }
  }
  //对生成的groups进行排序
  groups.sort((a, b) => b.surviveProbability - a.surviveProbability);
  message.value = `计算完成，在经过${iterationTimes}次的迭代后，最终的最短路径如下，总路程长度为${groups[0].distance}`
  buttonDisabled.value = true
  buttonMessage.value = "计算完成"
  canvas.value.updateCanvas(points, groups[0].route)
}
function refresh() {
  location.reload();
}
const message = ref("正在进行初始种群生成……");
const buttonDisabled = ref(true);
onMounted(() => {
  setTimeout(() => {
    message.value = "初始化后的种群中，存活率最高的一组如下，总路程长度为" + groups[0].distance;
    buttonDisabled.value = false;
  }, 4000);
});
</script>

<template><div class="header">
  <span>城市信息：</span>
  <ul class="cityList">
    <li v-for="(point, key) in points" :key="key">
      <div class="pointCircle" :style="{ background: point[2] }"></div>
      ({{ point[0] }},{{ point[1] }})
    </li>
  </ul>
</div>
<div>{{ message }}</div>
<Canvas ref="canvas" :width="width" :height="height" :points="points" :firstRoute="firstRoute" />
  <div>
    <button @click="refresh">重新生成（刷新）</button>
    <button @click="calculate" :disabled="buttonDisabled" v-text="buttonMessage"></button>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: center;
  align-content: center;
  flex-wrap: wrap;
}

canvas {
  border: 2px solid;
}

.cityList {
  display: flex;
}

.cityList li {
  margin-left: 40px;
  list-style: none;
  display: flex;
  align-items: center;
}

.pointCircle {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 3px solid black;
}

button {
  width: 300px;
  margin: 0 30px 0 30px;
}
</style>
