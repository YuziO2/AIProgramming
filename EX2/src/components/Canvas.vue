<script setup>
import { onMounted, reactive, ref } from "vue";
import { drawConcentricCircle, drawLine } from "../hooks/draw";

const props = defineProps({
  msg: String,
  width: Number,
  height: Number,
  points: Array,
  firstRoute: Array,
});

const myCanvas = ref(null);

onMounted(() => {
  const canvas = myCanvas.value;
  canvas.width = props.width * devicePixelRatio;
  canvas.height = props.height * devicePixelRatio;
  canvas.style.width = props.width + "px";
  canvas.style.height = props.height + "px";
  props.points.forEach((value) =>
    drawConcentricCircle(canvas, value[0], value[1], value[2])
  );
  setTimeout(() => {
    updateCanvas(props.points, props.firstRoute)
  }, 3000);
});

function updateCanvas(points, route, canvas = myCanvas.value) {
  const ctx = canvas.getContext("2d")
  ctx.reset()
  for (let i = 0; i < props.firstRoute.length - 1; i++) {
    drawLine(
      canvas,
      points[route[i]][0],
      points[route[i]][1],
      points[route[i + 1]][0],
      points[route[i + 1]][1]
    ); //画生成groups时最好的个体
  }
  drawLine(
    canvas,
    points[route[0]][0],
    points[route[0]][1],
    points[route[route.length - 1]][0],
    points[route[route.length - 1]][1]
  ); //首尾闭合
  points.forEach((value) =>
    drawConcentricCircle(canvas, value[0], value[1], value[2])
  ); //画点
}
defineExpose({ updateCanvas })
</script>

<template>
  <canvas ref="myCanvas"></canvas>
</template>

<style>
.read-the-docs {
  color: #888;
}
</style>
