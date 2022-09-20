<script setup>
import { reactive } from "vue";
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import Canvas from "./components/Canvas.vue";

const pointsNumber = 10; //城市数量
const points = []; //城市
const distances = []; //距离矩阵
const groupsNumber = 100; //种群数量
const groups = []; //种群
//路线类，route:Array;fitness,surviveProbability,distances:Number
function Route(route) {
  this.route = route;
  this.fitness = 0;
  this.surviveProbability = 0;
  this.distance = 0;
}

//画布大小
const width = 800;
const height = 600;
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
//对生成的groups进行排序
groups.sort((a, b) => b.surviveProbability - a.surviveProbability);
const firstRoute = groups[0].route; //并传给canvas进行绘制

function calculate() {
  console.log(groups);
}
function refresh() {
  location.reload();
}
</script>

<template>
  <div>
    <span>城市信息：</span>
    <ul class="cityList">
      <li v-for="(point, key) in points" :key="key">
        <div class="pointCircle" :style="{ background: point[2] }"></div>
        ({{ point[0] }},{{ point[1] }})
      </li>
    </ul>
  </div>
  <Canvas
    :width="width"
    :height="height"
    :points="points"
    :firstRoute="firstRoute"
  />
  <div>
    <button @click="refresh">重新生成（刷新）</button>
    <button @click="calculate">开始计算</button>
  </div>
</template>

<style scoped>
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
