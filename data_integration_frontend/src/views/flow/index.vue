<template>
  <div class="app-container">
    <flow-panel
      ref="flow-panel"
      :options-data="optionsData"
      :data.sync="processData"
      @saveData="setFlowData"
      @selectChange="selectChange"
    />
  </div>
</template>

<script>
import { fetchProjectCluster, fetchList, createData, updateData } from "@/api/datalink";
import FlowPanel from "@/components/ef/panel";
import lodash from "lodash";

export default {
  name: "Flow",
  components: { FlowPanel },
  data() {
    return {
      page: {
        field: "",
        model: 3,
        index: 1,
        limit: 1,
      },
      optionsData: [],
      flowData: {},
      processData: {
        name: "",
        nodeList: [],
        lineList: [],
      },
    };
  },
  mounted() {
    this.getList();
  },
  methods: {
    getList() {
      fetchProjectCluster().then((response) => {
        this.optionsData = response.items;
        setTimeout(() => {}, 1.5 * 1000);
      });
    },
    selectChange(index) {
      // this.handleChange(index.id)
      this.handleChange(index.id);
      // this.$nextTick
      // this.getFlowData(index)
    },
    handleChange(id) {
      if (this.flowData.pk === undefined) {
        this.getFlowData(id);
      } else {
        var name = this.processData.name;
        var temp = JSON.stringify(this.processData);
        console.log(this.flowData.isCreate, this.flowData);
        console.log(this.flowData.fields.name !== name, this.flowData.fields.name, name);
        console.log(
          this.flowData.fields.dataOfFlow !== temp,
          this.flowData.fields.dataOfFlow,
          temp
        );
        if (
          this.flowData.isCreate ||
          this.flowData.fields.name !== name ||
          this.flowData.fields.dataOfFlow !== temp
        ) {
          this.$confirm("当前内容已发生改变，是否保存数据", "提示", {
            confirmButtonText: "保存",
            cancelButtonText: "取消",
            type: "warning",
          })
            .then(() => {
              console.log("*****");
              console.log(name, temp);
              console.log("*****");
              this.setFlowData();
              this.$message({
                type: "success",
                message: "数据保存成功",
              });
              this.getFlowData(id);
            })
            .catch(() => {
              this.$message({
                type: "info",
                message: "更改数据未保存",
              });
              this.getFlowData(id);
            });
        } else {
          this.getFlowData(id);
        }
      }
    },
    setFlowData() {
      var name = this.processData.name;
      var temp = JSON.stringify(this.processData);
      if (this.flowData.isCreate) {
        this.createFlowData(name, temp);
      } else if (this.flowData.fields.dataOfFlow !== temp) {
        this.updateFlowData(name, temp);
      }
    },
    createFlowData(name, temp) {
      this.flowData.fields.name = name;
      this.flowData.fields.dataOfFlow = temp;
      console.log(this.flowData);
      createData(this.flowData).then((response) => {
        this.$notify({
          title: "Success",
          message: "Created Successfully",
          type: "success",
          duration: 2000,
        });
        this.flowData.isCreate = false;
      });
    },
    updateFlowData(name, value) {
      this.flowData.fields.name = name;
      this.flowData.fields.dataOfFlow = value;
      console.log(this.flowData);
      updateData(this.flowData).then((response) => {
        this.$notify({
          title: "Success",
          message: "Update Successfully",
          type: "success",
          duration: 2000,
        });
      });
    },
    getFlowData(id) {
      console.log(id);
      this.page.field = '{"clusterOfFlow":' + id + "}";
      fetchList(this.page).then((response) => {
        if (response.items[0] === undefined) {
          this.resetFlowData(id);
        } else {
          this.flowData = response.items[0];
          this.flowData.model = 3;
        }
        if (this.flowData.fields.dataOfFlow.length === 0) {
          this.resetProcessData();
          this.$notify({
            title: "Info",
            message: "The Flow is not exist,please create it now",
            type: "info",
            duration: 2000,
          });
        } else {
          console.log("has valid data");
          var temp = this.flowData.fields.dataOfFlow;
          // 不知道为什么，连续有效数据的话，vue就崩了
          // 好像是因为原来是浅拷贝，已换成深拷贝，不过未验证
          this.processData = lodash.cloneDeep(JSON.parse(temp));
          console.log("this.processData:", this.processData);
        }
        this.$nextTick(() => {
          // this.$refs['flow-panel'].loadEasyFlow()
          this.$refs["flow-panel"].flowChartReload();
        });
        setTimeout(() => {}, 1.5 * 1000);
      });
    },
    resetFlowData(id) {
      this.flowData = {
        isCreate: true,
        model: 3,
        fields: {
          clusterOfFlow: id,
          name: "UnName",
          dataOfFlow: "",
        },
      };
    },
    resetProcessData() {
      // var temp = JSON.stringify(data.fields.dataOfFlow)
      // eslint-disable-next-line no-new-object
      var temp = new Object({});
      temp.name = this.flowData.fields.name;
      temp.nodeList = [];
      temp.lineList = [];
      // this.processData = Object.assign({}, temp)
      this.processData = lodash.cloneDeep(temp);
      console.log(this.processData);
    },
  },
};
</script>

<style scoped></style>
