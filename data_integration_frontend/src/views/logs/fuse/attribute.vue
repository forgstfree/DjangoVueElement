<template>
  <div id="app-container">
    <DrawGraph
      v-bind:url="url"
      v-bind:height="height"
      v-bind:width="width"
    ></DrawGraph>
  </div>
</template>

<script>
import DrawGraph from "@/components/D3Draw/DrawGraph";
export default {
  name: "App",
  components: {
    DrawGraph,
  },
  data() {
    return {
      url: "100.json",
      title: "我的组件在App中被调用了",
      width: 1000,
      height: 700,
    };
  },
  methods: {
    changeTitle() {
      this.title = "我被改变了，两个组件都变了吗";
    },
  },
};
</script>

<style>
</style>
