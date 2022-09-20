<script setup>
import { onMounted, reactive, ref } from "vue";
import drawConcentricCircle from "../hooks/drawConcentricCircle";

const props = defineProps({
  msg: String,
  width: Number,
  height: Number,
  points: Array
});

const myCanvas = ref(null);

onMounted(() => {
  const canvas = myCanvas.value;
  canvas.width = props.width * devicePixelRatio;
  canvas.height = props.height * devicePixelRatio;
  canvas.style.width = props.width + "px";
  canvas.style.height = props.height + "px";
  props.points.forEach((value) => drawConcentricCircle(canvas, value[0], value[1],value[2]));
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
