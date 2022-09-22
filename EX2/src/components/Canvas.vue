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
    for (let i = 0; i < props.firstRoute.length - 1; i++) {
      drawLine(
        canvas,
        props.points[props.firstRoute[i]][0],
        props.points[props.firstRoute[i]][1],
        props.points[props.firstRoute[i + 1]][0],
        props.points[props.firstRoute[i + 1]][1]
      ); //画生成groups时最好的个体
    }
    drawLine(
      canvas,
      props.points[props.firstRoute[0]][0],
      props.points[props.firstRoute[0]][1],
      props.points[props.firstRoute[props.firstRoute.length - 1]][0],
      props.points[props.firstRoute[props.firstRoute.length - 1]][1]
    ); //首尾闭合
    props.points.forEach((value) =>
      drawConcentricCircle(canvas, value[0], value[1], value[2])
    ); //画点
  }, 4000);
});
</script>

<template>
  <canvas ref="myCanvas"></canvas>
</template>

<style>
.read-the-docs {
  color: #888;
}
</style>
