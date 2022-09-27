# 人工智能实验二

本实验由Javascript+vue框架写成，打包工具为Vite，包管理器为pnpm。

要启动程序，请先安装nodejs，再使用`npm i pnpm -g`全局安装pnpm，然后在项目目录下执行`pnpm i`，然后执行`pnpm dev`，打开在终端显示的网址，即可进入程序可视化运行界面。

当然，我也打包好了一份可以直接运行的构建版本，只需将`/dist`中的内容放入本地的静态服务器中，访问该服务器，即可进入程序可视化运行界面。例如，在`/dist`目录下，执行`python3 -m http.server 3000`，即可在<http://localhost:3000>下运行程序。

程序主要代码位于`src/App.vue`中

# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

## Recommended IDE Setup

- [VS Code](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar)
