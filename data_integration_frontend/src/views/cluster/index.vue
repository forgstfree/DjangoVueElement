<template>
  <div class="app-container">
    <div>
      <el-row>
        <el-col :span="12">
          <div>
            <h3><span>集群</span></h3>
          </div>
        </el-col>
        <el-col :span="8">
          <div>
            <span>项目:</span>
            <el-select
              v-model="idOfProject"
              filterable
              clearable
              placeholder="选择项目"
              @change="projectChange($event)"
            >
              <el-option
                v-for="item in briefOfProjectList"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </div>
        </el-col>
        <el-col :span="4">
          <div style="float: right">
            <el-button type="primary" icon="el-icon-plus" @click="handleCreate"
              >新建集群</el-button
            >
          </div>
        </el-col>
      </el-row>
    </div>
    <div>
      <h4 style="color: #20a0ff">管理集群</h4>
      <el-table
        :data="list"
        :default-sort="{ prop: 'fields.lastAccessed', order: 'descending' }"
        border
        style="width: 100%"
      >
        <el-table-column prop="name" label="名称" sortable min-width="1" align="center">
          <template slot-scope="{ row }">
            <span>{{ row.fields.name }}</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="description"
          label="描述"
          sortable
          min-width="3"
          align="center"
        >
          <template slot-scope="{ row }">
            <span>{{ row.fields.description }}</span>
          </template>
        </el-table-column>
        <!-- <el-table-column
          prop="nodes"
          label="数据源数量"
          sortable
          min-width="2"
          align="center"
        >
          <template slot-scope="{ row }">
            <span>{{ row.fields.nodes }}</span>
          </template>
        </el-table-column> -->
        <el-table-column
          prop="autoSuspend"
          label="触发方式"
          sortable
          min-width="3"
          align="center"
        >
          <template slot-scope="{ row }">
            <el-row>
              <el-col :span="8">
                <div style="padding-top: 4px">
                  <el-tag :type="row.fields.autoSuspend | statusFilter">
                    {{ triggerOptions[row.fields.autoSuspend].label }}
                  </el-tag>
                </div>
              </el-col>
              <el-col :span="16"
                ><div>
                  <el-input v-model="row.fields.date" :disabled="true" /></div
              ></el-col>
            </el-row>
          </template>
        </el-table-column>
        <el-table-column
          prop="statusOfCluster"
          label="状态"
          sortable
          min-width="1"
          align="center"
        >
          <template slot-scope="{ row }">
            <el-tag :type="row.fields.statusOfCluster | statusFilter">
              {{ statusMap[row.fields.statusOfCluster] }}
            </el-tag>
          </template></el-table-column
        >
        <el-table-column
          prop="lastAccessed"
          label="最近更新"
          sortable
          min-width="2"
          align="center"
        >
          <template slot-scope="{ row }">
            <span>{{ row.fields.lastAccessed }}</span>
          </template>
        </el-table-column>
        <el-table-column label="动作" min-width="3" align="center">
          <template slot-scope="{ row, $index }">
            <el-button size="mini" type="primary" @click="handleUpdate(row)">
              Edit
            </el-button>
            <el-button
              v-if="row.fields.statusOfCluster == 0"
              size="mini"
              type="success"
              @click="handleModifyStatus(row, 'start')"
            >
              START
            </el-button>
            <el-button
              v-if="row.fields.statusOfCluster == 1"
              size="mini"
              @click="handleModifyStatus(row, 'end')"
            >
              END
            </el-button>
            <el-button size="mini" type="danger" @click="handleDelete(row, $index)">
              Delete
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <pagination
      v-show="total > 0"
      :limit.sync="page.limit"
      :page.sync="page.index"
      :total="total"
      @pagination="getList"
    />
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form
        ref="dataForm"
        :model="temp"
        :rules="rules"
        label-position="left"
        label-width="120px"
        style="width: 400px; margin-left: 50px"
      >
        <el-form-item label="Name" prop="name">
          <el-input v-model="temp.fields.name" />
        </el-form-item>
        <el-form-item label="Project">
          <el-input
            v-model="temp.fields.projectOfCluster"
            :disabled="idOfProject !== ''"
          />
        </el-form-item>
        <el-form-item label="Auto Suspend">
          <el-row>
            <el-col :span="8">
              <el-select v-model="temp.fields.autoSuspend" clearable placeholder="请选择">
                <el-option
                  v-for="item in triggerOptions"
                  :key="item.id"
                  :label="item.label"
                  :value="item.id"
                />
              </el-select>
            </el-col>
            <el-col :span="16"
              ><div>
                <el-input
                  v-model="temp.fields.date"
                  placeholder="分 时 日 月 周/年"
                /></div
            ></el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="Status">
          <el-select v-model="temp.fields.statusOfCluster" @change="testChange">
            <el-option
              v-for="item in statusOptions"
              :key="item.id"
              :label="item.status"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Description" prop="description">
          <el-input
            v-model="temp.fields.description"
            :autosize="{ minRows: 2, maxRows: 4 }"
            type="textarea"
            placeholder="Please Input"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false"> Cancel </el-button>
        <el-button
          type="primary"
          @click="dialogStatus === 'create' ? createData() : updateData()"
        >
          Confirm
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  createData,
  fetchList,
  fetchBrief,
  updateData,
  deleteData,
  startScheduler,
} from "@/api/datalink";
import Pagination from "@/components/Pagination";
import lodash from "lodash";
export default {
  name: "Cluster",
  components: { Pagination },
  filters: {
    statusFilter(status) {
      const statusMap = {
        0: "info",
        1: "success",
        2: "danger",
        3: "warning",
        deleted: "danger",
      };
      return statusMap[status];
    },
    // typeFilter(type) {
    //   return calendarTypeKeyValue[type]
    // }
  },
  data() {
    return {
      value: "",
      list: [],
      total: 10,
      idOfProject: "",
      brief: {
        model: 1,
        values: ["id", "name"],
      },
      briefOfProjectList: [],
      page: {
        field: "",
        model: 2,
        index: 1,
        limit: 10,
      },
      listLoading: true,
      temp: {
        pk: undefined,
        model: "",
        fields: {
          name: "",
          description: "",
          autoSuspend: "",
          statusOfCluster: "",
          projectOfCluster: "",
        },
      },
      dialogVisible: false,
      dialogStatus: "",
      textMap: {
        update: "Edit",
        create: "Create",
      },
      statusOptions: [
        { id: 0, status: "END" },
        { id: 1, status: "START" },
      ],
      triggerOptions: [
        { id: 0, label: "NULL" },
        { id: 1, label: "date" },
        { id: 2, label: "interval" },
        { id: 3, label: "cron" },
      ],
      statusMap: {
        0: "END",
        1: "START",
      },
      rules: {},
    };
  },
  created() {
    this.getBrief();
    this.getList();
  },
  methods: {
    getBrief() {
      fetchBrief(this.brief).then((response) => {
        // console.log(response.items)
        // console.log(typeof response.items)
        this.briefOfProjectList = JSON.parse(response.items);
        setTimeout(() => {
          this.listLoading = false;
        }, 1.5 * 1000);
      });
    },
    getList() {
      this.listLoading = true;
      fetchList(this.page).then((response) => {
        this.list = response.items;
        this.total = response.total;
        setTimeout(() => {
          this.listLoading = false;
        }, 1.5 * 1000);
      });
    },
    resetTemp() {
      this.temp = {
        pk: undefined,
        model: 2,
        fields: {
          name: "",
          description: "",
          autoSuspend: "",
          projectOfCluster: this.idOfProject,
        },
      };
      // if (this.idOfProject !== '') {
      //   this.temp.fields.projectOfCluster = this.idOfProject
      // }
    },
    handleCreate() {
      this.resetTemp();
      this.dialogStatus = "create";
      this.dialogVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    createData: function () {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          createData(this.temp).then((response) => {
            this.dialogVisible = false;
            this.getList();
            this.$notify({
              title: "Success",
              message: "Created Successfully",
              type: "success",
              duration: 2000,
            });
          });
        }
      });
    },
    handleUpdate(row) {
      // this.temp = Object.assign({}, row) // copy obj
      this.temp = lodash.cloneDeep(row);
      this.temp.model = 2;
      this.dialogStatus = "update";
      this.dialogVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    updateData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp);
          updateData(tempData).then(() => {
            this.dialogVisible = false;
            this.getList();
            this.$notify({
              title: "Success",
              message: "Update Successfully",
              type: "success",
              duration: 2000,
            });
          });
        }
      });
    },
    handleDelete(row, index) {
      this.page.field = '{"id":' + row.pk + "}";
      deleteData(this.page).then((response) => {
        this.$notify({
          title: "Success",
          message: "Delete Successfully",
          type: "success",
          duration: 2000,
        });
        this.list.splice(index, 1);
      });
    },
    handleModifyStatus(row, status) {
      console.log(row, status);
      if (status === "end") {
        row.fields.statusOfCluster = 0;
      } else {
        row.fields.statusOfCluster = 1;
      }
      this.temp = lodash.cloneDeep(row);
      this.temp.model = 2;
      const tempData = Object.assign({}, this.temp);
      updateData(tempData).then(() => {
        this.getList();
        this.$notify({
          title: "Success",
          message: "Update Successfully",
          type: "success",
          duration: 2000,
        });
      });
      var tempId = {
        id: row.pk,
      };
      startScheduler(tempId).then(() => {
        console.log(tempId);
        this.$notify({
          title: "Success",
          message: "Start Scheduler Successfully",
          type: "success",
          duration: 2000,
        });
      });
    },
    statusFormat(row, column, cellValue) {
      return this.statusMap[cellValue];
      // return this.statusMap[];
    },
    projectChange(index) {
      // this.temp.fields.projectOfCluster = index
      if (index === "") {
        this.page.field = "";
      } else {
        this.page.field = '{"projectOfCluster":' + index + "}";
      }
      this.getList();
    },
    triggerChange(index) {
      if (index === "") {
        console.log(index);
      }
    },
    testChange(index) {
      console.log(index);
    },
  },
};
</script>

<style scoped></style>
