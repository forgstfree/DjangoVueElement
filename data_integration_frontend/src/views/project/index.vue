<template>
  <div class="project-container">
    <div class="project-title">
      <el-row class="my-row">
        <el-col :span="12">
          <div>
            <h3><span>项目</span></h3>
          </div>
        </el-col>
        <el-col :span="12">
          <div style="float: right">
            <el-button icon="el-icon-plus" type="primary" @click="handleCreate"
              >新建项目</el-button
            >
          </div>
        </el-col>
      </el-row>
    </div>
    <div>
      <h4 style="color: #20a0ff">管理项目</h4>
      <el-table
        :data="list"
        :default-sort="{ prop: 'fields.lastAccessed', order: 'descending' }"
        border
        style="width: 100%"
      >
        <el-table-column
          label="名称"
          min-width="1"
          prop="fields.name"
          sortable
          align="center"
        />
        <el-table-column
          label="所属机构"
          min-width="1"
          prop="fields.businessUnit"
          sortable
          align="center"
        />
        <el-table-column
          label="描述"
          min-width="2"
          prop="fields.description"
          sortable
          align="center"
        />
        <el-table-column
          label="最近更新"
          min-width="2"
          prop="fields.lastAccessed"
          sortable
          align="center"
        />
        <el-table-column label="动作" min-width="2" prop="date" align="center">
          <template slot-scope="{ row, $index }">
            <el-button size="mini" type="primary" @click="handleUpdate(row)">
              Edit
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
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form
        ref="dataForm"
        :model="temp"
        :rules="rules"
        label-position="left"
        label-width="120px"
        style="width: 400px; margin-left: 50px"
      >
        <el-form-item label="Name" prop="fields.name">
          <el-input v-model="temp.fields.name" />
        </el-form-item>
        <el-form-item label="Business Unit" prop="fields.businessUnit">
          <el-input v-model="temp.fields.businessUnit" />
        </el-form-item>
        <el-form-item label="Description" prop="fields.description">
          <el-input
            v-model="temp.fields.description"
            :autosize="{ minRows: 2, maxRows: 4 }"
            type="textarea"
            placeholder="Please input"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false"> Cancel </el-button>
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
import { createData, fetchList, updateData, deleteData } from "@/api/datalink";
import Pagination from "@/components/Pagination";

export default {
  name: "Project",
  components: { Pagination },
  data() {
    return {
      list: [],
      total: 10,
      page: {
        // 这里加field是为了和后续页面需要field保持一致性，是一个多余的key
        field: "",
        model: 1,
        index: 1,
        limit: 10,
      },
      listLoading: true,
      temp: {
        pk: undefined,
        model: "",
        fields: {
          name: "",
          businessUnit: "",
          description: "",
          lastAccessed: "",
        },
      },
      dialogFormVisible: false,
      dialogStatus: "",
      textMap: {
        update: "Edit",
        create: "Create",
      },
      rules: {
        "fields.name": [
          { required: true, message: "name is required", trigger: "change" },
        ],
        "fields.businessUnit": [
          {
            required: true,
            message: "businessUnit is required",
            trigger: "change",
          },
        ],
        "fields.description": [
          {
            required: true,
            message: "description is required",
            trigger: "blur",
          },
        ],
      },
    };
  },
  created() {
    this.getList();
  },
  methods: {
    getList() {
      this.listLoading = true;
      fetchList(this.page).then((response) => {
        this.list = response.items;
        this.total = response.total;
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false;
        }, 1.5 * 1000);
      });
    },
    resetTemp() {
      this.temp = {
        pk: undefined,
        model: 1,
        fields: {
          name: "",
          businessUnit: "",
          description: "",
          lastAccessed: "",
        },
      };
    },
    handleCreate() {
      this.resetTemp();
      this.dialogStatus = "create";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    createData: function () {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          createData(this.temp).then((response) => {
            this.dialogFormVisible = false;
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
      this.temp = Object.assign({}, row); // copy obj
      this.temp.model = 1;
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    updateData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp);
          updateData(tempData).then(() => {
            this.dialogFormVisible = false;
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
      this.page.field = '{"pk":' + row.pk + "}";
      deleteData(this.page).then((response) => {
        this.$notify({
          title: "Success",
          message: "Delete Successfully",
          type: "success",
          duration: 2000,
        });
        this.page.field = "";
        this.list.splice(
          this.list.findIndex((item) => item.pk === row.pk),
          1
        );
      });
    },
  },
};
</script>

<style scoped>
.project-container {
  margin-left: 20px;
  margin-right: 20px;
}

.project-title {
  /*background-color: #d3dce6;*/
}

.my-row {
  display: flex;
  align-items: center;
  /*justify-content: center;*/
}
</style>
