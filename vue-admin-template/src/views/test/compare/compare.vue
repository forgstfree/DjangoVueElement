<template>
  <div class="demo-image">
    <el-row>
      <el-col :span="6" :offset="4"
        ><span class="demonstration">普通ER图</span></el-col
      >
      <el-col :span="6" :offset="4"
        ><span class="demonstration">增强ER图</span></el-col
      >
    </el-row>
    <el-row>
      <el-col :span="12">
        <DrawGraph :filename="logresult[0]"></DrawGraph>
      </el-col>
      <el-col :span="12">
        <DrawGraph :filename="logresult[1]"></DrawGraph>
      </el-col>
    </el-row>
  </div>
</template>
<script>
export default {
  components: {
    DrawGraph: () => import("@/components/D3Draw/DrawGraph.vue"),
  },
  data() {
    return {
      fits: ["fill", "contain", "cover", "none", "scale-down"],
      logresult: ["result/CommonER.json","result/EnhanceER.json","result/25ubuntu_VWhlzfn.log.json"],

      erurl: "http://10.9.21.98:13333/media/showsvg/ERa.svg",
      noterurl: "http://10.9.21.98:13333/media/showsvg/ERb.svg",
    };
  },
};
</script>

<style>
.demonstration {
  margin-top: 20px;
  display: block;
  color: #8492a6;
  font-size: 14px;
  margin-bottom: 2px;
}
.block {
  height: 800px;
  width: 50%;
}
</style>