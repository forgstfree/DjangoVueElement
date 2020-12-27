<template>
  <div class="app-container">
    <app-progect>
      <div>
        <el-row>
          <el-col :span="8">
            <div>
              <h4><span>Connections</span></h4>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <span>Project:</span>
              <el-select v-model="value" placeholder="Choose Project">
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <span>Cluster:</span>
              <el-select v-model="value" placeholder="Choose Cluster">
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </div>
          </el-col>
          <el-col :span="4">
            <div>
              <el-button type="primary" icon="el-icon-plus">New Connection</el-button>
            </div>
          </el-col>
        </el-row>
      </div>
      <div>
        <h5>Manage Connections</h5>
        <el-table
          :data="tableData"
          style="width: 100%"
          :default-sort="{prop: 'date', order: 'descending'}"
        >
          <el-table-column
            prop="date"
            label="Action"
            sortable
            width="180">
          </el-table-column>
          <el-table-column
            prop="name"
            label="Name"
            sortable
            width="180">
          </el-table-column>
          <el-table-column
            prop="name"
            label="Description"
            sortable
            width="180">
          </el-table-column>
          <el-table-column
            prop="address"
            label="Last Accessed"
            :formatter="formatter">
          </el-table-column>
        </el-table>
      </div>
    </app-progect>
  </div>
</template>

<script>
  export default {}
</script>

<style scoped>
  .line {
    text-align: center;
  }
</style>

