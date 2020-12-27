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
    };
  },

  mounted: function () {
    this.showLogsList();
  },
  methods: {
    setCurrent(val) {
      this.currentfile = val;
      console.log(val);
    },
    showLogsList() {
      this.$http
        .get("http://10.9.21.98:13333/dblog/show_data/", {
          params: { num: 10 },
        })
        .then((response) => {
          var res = JSON.parse(response.bodyText);
          console.log(res);
          if (res.code === 20000) {
            this.tableData = res.items;
          } else {
            this.$message.error("查询数据源失败");
            console.log(res["msg"]);
          }
        });
    },
    getLogJson() {
      this.$http
        .get("http://10.9.21.98:13333/dblog/analysislog/", {
          params: { filename: this.currentfile, linenum: "100" },
        })
        .then((response) => {
          var res = JSON.parse(response.bodyText);
          if (res.code === 20000) {
            this.logresult = res["jsonfiles"][0];
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
