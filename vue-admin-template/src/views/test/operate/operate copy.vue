<template>
  <div>
    <el-table
      ref="singleTable"
      :data="tableData"
      highlight-current-row
      @current-change="handleCurrentChange"
      style="width: 100%"
    >
      <el-table-column type="index" width="50"> </el-table-column>
      <el-table-column property="pk" label="编号" width="120">
      </el-table-column>
      <el-table-column property="fields.file" label="文件" width="220">
      </el-table-column>
      <el-table-column property="fields.uploaded_at" label="上传时间">
      </el-table-column>
    </el-table>
    <div style="margin-top: 20px">
      <!-- <el-button @click="setCurrent(tableData[1])">选中第二行</el-button> -->
      <el-button @click="setCurrent()">取消选择</el-button>
      <el-button @click="getLogJson()">确定</el-button>
      <el-button @click="show = true">show DrawGraph</el-button>
    </div>
    <div v-if="show">
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
      currentRow: null,
      logresult: "",
    };
  },

  mounted: function () {
    this.showLogsList();
  },
  methods: {
    setCurrent(row) {
      this.$refs.singleTable.setCurrentRow(row);
    },
    handleCurrentChange(val) {
      this.currentRow = val;
      if (val != null )
        this.currentfile = this.currentRow.fields.file;
      // console.log(this.currentRow)
      // console.log(val.fields.file)
    },
    showLogsList() {
      this.$http
        .get("http://10.9.21.98:13333/dblog/show_data/", { params: { num: 3 } })
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
      this.$http
        .get("http://10.9.21.98:13333/dblog/analysislog/", {
          params: { filename: this.currentfile, linenum: "100" },
        })
        .then(response => {
          var res = JSON.parse(response.bodyText);
          if (res.error_num === 0) {
            this.logresult = res['jsonfiles'][0]
            this.show = true
          }
          else {
            console.log("获取文件分析结果失败")
            console.log(res)
          }
        });
    },
  },
};
</script>