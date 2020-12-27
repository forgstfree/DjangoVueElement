<template>
  <div class="home">
    <el-row>
      <el-table :data="dataList" style="width: 100%" border>
        <el-table-column prop="id" label="编号" min-width="100">
          <template slot-scope="scope"> {{ scope.row.pk }} </template>
        </el-table-column>
        <el-table-column prop="book_name" label="文件名" min-width="100">
          <template slot-scope="scope"> {{ scope.row.fields.name }} </template>
        </el-table-column>
        <el-table-column prop="add_time" label="添加时间" min-width="100">
          <template slot-scope="scope">
            {{ scope.row.fields.uploaded_at }}
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "home",
  data() {
    return {
      input: "",
      dataList: [],
    };
  },
  mounted: function () {
    this.showBooks();
  },
  methods: {
    showBooks() {
      this.$http
        .get("http://10.9.21.98:13333/dblog/show_data/", { params: { num: 0 } })
        .then((response) => {
          var res = JSON.parse(response.bodyText);
          console.log(response);
          if (res.code === 20000) {
            this.dataList = res["items"];
          } else {
            this.$message.error("查询数据源失败");
            console.log(res["msg"]);
          }
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
