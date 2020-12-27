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
        ><div class="grid-content bg-purple">
          <el-button
            type="success"
            @click="getLogJson()"
            icon="el-icon-check"
            circle
          ></el-button></div
      ></el-col>
    </el-row>
    <div v-if="show" style="margin-top: 20px" class="height:100% width=100%">
      <DrawGraph :filename="logresult"></DrawGraph>
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
      tableData: [],
      logresult: "",
      page: {
        // model: 2,
        all: false,
        index: 1,
        limit: 10,
      },
      params: {
        filename: "",
        linenum: "100",
      },
      value: "",
    };
  },

  mounted: function () {
    this.getList();
  },
  methods: {
    setCurrent(val) {
      this.params.filename = val;
      console.log(val);
    },
    getList() {
      console.log("getList");
      fetchList(this.page).then((response) => {
        console.log(response);
        this.tableData = response.items;
      });
    },
    getLogJson() {
      analysisLog(this.params).then((response) => {
        console.log(response);
        this.logresult = response.jsonfiles[0];
        this.show = true;
      });
    },
  },
};
</script>
