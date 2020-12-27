<template>
  <div class="home">
    <div>
      <h3 style="color: #20a0ff"><span>日志文件列表</span></h3>
    </div>
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
    <pagination
      v-show="total > 0"
      :limit.sync="page.limit"
      :page.sync="page.index"
      :total="total"
      @pagination="showLogsList"
    />
  </div>
</template>

<script>
import { fetchList } from "@/api/logs";
import Pagination from "@/components/Pagination";

export default {
  name: "home",
  components: { Pagination },
  data() {
    return {
      input: "",
      dataList: [],
      total: 0,
      page: {
        all: false,
        index: 1,
        limit: 10,
      },
    };
  },
  created() {
    this.showLogsList();
  },
  methods: {
    showLogsList() {
      console.log("getList");
      fetchList(this.page).then((response) => {
        // var res = JSON.parse(response.bodyText);
        console.log(response);
        this.dataList = response.items;
        this.total = response.total;
      });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home {
  margin-left: 20px;
  margin-right: 20px;
}
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
