<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="6"
        ><div class="grid-content bg-purple">
          <el-select v-model="value" placeholder="请选择" @change="setCurrent">
            <el-option
              v-for="item in tableData"
              :key="item.pk"
              :label="item.fields.name"
              :value="item.fields.file"
            >
            </el-option>
          </el-select></div
      ></el-col>
      <el-col :span="6"
        ><div>
          <el-slider v-model="value1" range :max="100"> </el-slider></div
      ></el-col>
      <el-col :span="6"
        ><div class="grid-content bg-purple">
          <el-button
            type="success"
            @click="getLogJson()"
            icon="el-icon-check"
            circle
          ></el-button></div
      ></el-col>
    </el-row>
    <div v-if="show" style="margin-top: 20px">
      <DrawGraph :filename="logresult" :key="logresult"></DrawGraph>
    </div>
  </div>
</template>

<script>
import { fetchList, analysisLog } from "@/api/logs";
export default {
  components: {
    DrawGraph: () => import("@/components/D3Draw/DrawGraph.vue"),
  },
  data() {
    return {
      show: false,
      currentfile: "",
      tableData: [],
      logresult: "",
      value: "",
      value1: [0, 50],
      range1: 100,
      page: {
        all: true,
        index: 1,
        limit: 10,
      },
      params: {
        filename: "",
        linenum: "100",
      },
    };
  },

  mounted: function () {
    this.showLogsList();
  },
  methods: {
    setCurrent(val) {
      this.params.filename = val;
      console.log(val);
    },
    showLogsList() {
      fetchList(this.page).then((response) => {
        this.tableData = response.items;
      });
    },
    getLogJson() {
      this.params.linenum = Math.abs(this.value1[1] - this.value1[0]);
      analysisLog(this.params).then((response) => {
        this.logresult = response.jsonfiles[0];
        this.show = true;
      });
    },
  },
};
</script>
