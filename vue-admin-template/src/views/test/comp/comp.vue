<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="5"
        ><div class="grid-content bg-purple">
          <el-select v-model="currentvalue1" placeholder="请选择" @change="setCurrent1">
            <el-option
              v-for="item in tableData"
              :key="item.pk"
              :label="item.fields.name"
              :value="item.fields.file"
            >
            </el-option>
          </el-select></div
      ></el-col>
      <el-col :span="5"
        ><div>
          <el-slider v-model="valuerange1" range :max="100"> </el-slider></div
      ></el-col>
      <el-col :span="5"
        ><div class="grid-content bg-purple">
          <el-select v-model="currentvalue2" placeholder="请选择" @change="setCurrent2">
            <el-option
              v-for="item in tableData"
              :key="item.pk"
              :label="item.fields.name"
              :value="item.fields.file"
            >
            </el-option>
          </el-select></div
      ></el-col>
      <el-col :span="5"
        ><div>
          <el-slider v-model="valuerange2" range :max="100"> </el-slider></div
      ></el-col>
      <el-col :span="4"
        ><div class="grid-content bg-purple">
          <el-button
            type="success"
            @click="getLogJson()"
            icon="el-icon-check"
            circle
          ></el-button></div
      ></el-col>
    </el-row>
    <el-row>
      <el-col :span="12"
        ><div v-if="show" style="margin-top: 20px">
          <DrawGraph :filename="logresult1" :key="logresult1"></DrawGraph></div
      ></el-col>
      <el-col :span="12">
        <div v-if="show" style="margin-top: 20px">
          <DrawGraph :filename="logresult2" :key="logresult2"></DrawGraph></div
      ></el-col>
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
      show: false,
      currentfile1: "",
      currentfile2: "",
      tableData: [],
      logresult1: "",
      logresult2: "",
      currentvalue1: "",
      currentvalue2: "",
      valuerange1: [0, 50],
      valuerange2: [0, 50],
      range1: 50,
      range2: 50,
    };
  },

  mounted: function () {
    this.showLogsList();
  },
  methods: {
    setCurrent1(val) {
      this.currentfile1 = val;
      console.log(val);
    },
    setCurrent2(val) {
      this.currentfile2 = val;
      console.log(val);
    },
    showLogsList() {
      this.$http
        .get("http://10.9.21.98:13333/dblog/show_data/", {
          params: { num: 10 },
        })
        .then((response) => {
          var res = JSON.parse(response.bodyText);
          if (res.error_num === 0) {
            this.tableData = res["list"];
          } else {
            this.$message.error("查询数据源失败");
            console.log(res["msg"]);
          }
        });
    },
    getLogJson() {
      this.range1 = Math.abs(this.valuerange1[1] - this.valuerange1[0]);
      this.range2 = Math.abs(this.valuerange2[1] - this.valuerange2[0]);
      // console.log(this.range1)
      // console.log(this.range2)
      this.$http
        .get("http://10.9.21.98:13333/dblog/analysislog/", {
          params: { filename: this.currentfile1, linenum: this.range1 },
        })
        .then((response) => {
          var res = JSON.parse(response.bodyText);
          if (res.error_num === 0) {
            this.logresult1 = res["jsonfiles"][0];
            // this.show = true;
          } else {
            console.log("获取文件分析结果失败");
            console.log(res);
          }
        });
      this.$http
        .get("http://10.9.21.98:13333/dblog/analysislog/", {
          params: { filename: this.currentfile2, linenum: this.range2 },
        })
        .then((response) => {
          var res = JSON.parse(response.bodyText);
          if (res.error_num === 0) {
            this.logresult2 = res["jsonfiles"][0];
            this.show = true;
          } else {
            console.log("获取文件分析结果失败");
            console.log(res);
          }
        });
    },
  },
};
</script>