<script setup>
import { reactive } from "vue";
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import Canvas from "./components/Canvas.vue";
const points = [];
const width = 800;
const height = 600;
const pointsLength = 10;
for (let i = 0; i < pointsLength; i++) {
  points.push([
    Math.floor(
      30 + ((Math.random() * 10000) % (width * devicePixelRatio - 60))
    ),
    Math.floor(
      30 + ((Math.random() * 10000) % (height * devicePixelRatio - 60))
    ),
    getRandomColor(),
  ]);
}
function getRandomColor() {
  var color =
    "#" +
    Math.floor(Math.random() * 0xffffff)
      .toString(16)
      .padStart(6, "0");
  return color;
}
</script>

<template>
  <div>
    <span>城市信息：</span>
    <ul class="cityList">
      <li v-for="(point, key) in points" :key="key">
        <div class="pointCircle" :style="{'background':point[2]}"></div>
        ({{ point[0] }},{{ point[1] }})
      </li>
    </ul>
  </div>
  <Canvas :width="width" :height="height" :points="points" />
  <button>开始计算</button>
</template>

<style scoped>
canvas{
  border: 2px solid
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
button{
  width: 500px;
}
</style>
