<script setup>
import { ref, onMounted } from "vue";
import { cloneDeep } from 'lodash'
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import Canvas from "./components/Canvas.vue";
const canvas = ref()

const pointsNumber = 10; //城市数量
const points = []; //城市
const distances = []; //距离矩阵
const groupsNumber = 100; //种群数量
let groups = []; //种群
const sonNumber = 32;
const sonGroup = [];
let iterationTimes = 1000; //迭代次数
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
function calculateGroup(group) {
  let totalFitness = 0;
  for (let i = 0; i < group.length; i++) {
    let totalDistance = 0;
    for (let j = 0; j < pointsNumber - 1; j++)
      totalDistance += distances[group[i].route[j]][group[i].route[j + 1]];
    group[i].distance = totalDistance;
    group[i].fitness = 1 / totalDistance; //个体的适应度为其总距离的倒数
    totalFitness += group[i].fitness;
  }
  //计算每个个体的生存概率（被选择概率）,为个体适应度 / 总适应度
  for (let i = 0; i < group.length; i++)
    group[i].surviveProbability = group[i].fitness / totalFitness;
}
calculateGroup(groups);

//对生成的groups进行排序
groups.sort((a, b) => b.surviveProbability - a.surviveProbability);
const initGroup = cloneDeep(groups)
const firstRoute = ref(groups[0].route); //并传给canvas进行绘制

const buttonMessage = ref("开始计算");

//计算累计的概率，利用赌轮选择法，随机生成0~1之间一个数，根据计算出来的累计概率选择个体
function selectPoint() {
  let totalProbability = 0
  for (let i = 0; i < groupsNumber; i++) {
    totalProbability += groups[i].surviveProbability
    if (Math.random() < totalProbability)
      return i
  }
}

function calculate() {
  iterationTimes = prompt("请输入迭代次数，默认1000：", 1000)
  while (!/^[0-9]*[1-9][0-9]*$/.test(iterationTimes)) {
    alert("非法输入！请输入正整数！")
    iterationTimes = prompt("请输入迭代次数，默认1000：", 1000)
  }
  debugger
  iterationTimes = parseInt(iterationTimes)
  groups = cloneDeep(initGroup)
  buttonDisabled.value = true;
  buttonMessage.value = "计算中，请稍后……"
  setTimeout(() => {
    for (let i = 0; i < iterationTimes; i++) {
      for (let j = 0; j < sonNumber; j++) {
        //选择开始
        let fatherIndex = selectPoint()
        let matherIndex = selectPoint()
        while (fatherIndex == matherIndex)//防止自交
          matherIndex = selectPoint()
        let Father = cloneDeep(groups[fatherIndex])
        let Mather = cloneDeep(groups[matherIndex])
        //选择结束，交叉开始
        //在交叉率以内，则交叉
        if (Math.random() < crossRate) {
          let changeNumber = Math.floor(
            ((Math.random() * pointsNumber * 10) % (pointsNumber / 2)) + 1
          );
          let changePoint = Math.floor((Math.random() * pointsNumber * 10) % (pointsNumber - changeNumber))  //交叉点
          let map = new Map()
          for (let k = changePoint; k < changeNumber + changePoint; k++) {//建立不重复的映射
            let temp1 = Father.route[k]
            let temp2 = Mather.route[k]
            Father.route[k] = temp2
            Mather.route[k] = temp1//交换
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
            if (map.has(Father.route[k]))
              Father.route[k] = map.get(Father.route[k])
            if (map.has(Mather.route[k]))
              Mather.route[k] = map.get(Mather.route[k])
          }
          sonGroup.push(Father)
          sonGroup.push(Mather)
        }
      }
      //变异
      //每个子实例都有可能基因（路径）多次变换
      for (let j = 0; j < sonNumber; j++) {
        if (Math.random() < mutationRate) {
          for (let exchangeTime = Math.floor(Math.random() * pointsNumber + 1); exchangeTime > 0; exchangeTime--) {
            const changePointA = Math.floor(Math.random() * pointsNumber)
            const changePointB = Math.floor(Math.random() * pointsNumber)
            const temp = sonGroup[j].route[changePointA]
            sonGroup[j].route[changePointA] = sonGroup[j].route[changePointB]
            sonGroup[j].route[changePointB] = temp
          }
        }
      }
      //计算子种群的各项参数
      calculateGroup(sonGroup)
      //合入原种群
      sonGroup.forEach(v => groups.push(v))
      sonGroup.splice(0)
      //选优
      groups.sort((a, b) => b.surviveProbability - a.surviveProbability)
      //丢弃后面的
      groups.splice(groupsNumber)
    }
    message.value = `计算完成，在经过${iterationTimes}次的迭代后，最终的最短路径如下，总路程长度为${groups[0].distance}`
    buttonDisabled.value = true
    buttonMessage.value = "以新的迭代次数重新计算"
    canvas.value.updateCanvas(points, groups[0].route)
    buttonDisabled.value = false
  }, 10)
}
function refresh() {
  location.reload();
}
function backToInit() {
  groups = cloneDeep(initGroup)
  message.value = "初始化后的种群中，存活率最高的一组如下，总路程长度为" + groups[0].distance;
  canvas.value.updateCanvas(points, groups[0].route)
}
const message = ref("正在进行初始种群生成……");
const buttonDisabled = ref(true);
onMounted(() => {
  setTimeout(() => {
    message.value = "初始化后的种群中，存活率最高的一组如下，总路程长度为" + groups[0].distance;
    buttonDisabled.value = false;
  }, 3000);
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
    <button @click="backToInit">恢复初始</button>
    <button @click="calculate" :disabled="buttonDisabled">{{buttonMessage}}</button>
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
