<template>
  <div class="upload-container">
    <el-upload
      :data="dataObj"
      :multiple="false"
      :show-file-list="false"
      class="file-uploader"
      drag
      action="http://10.9.21.98:13333/dblog/upload/"
      :before-upload="beforeUpload"
      :on-success="uploadSuccess"
    >
      <i class="el-icon-upload" />
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
    </el-upload>
    <div>
      <el-input placeholder="请输入内容" v-model="input1">
        <template slot="prepend">文件名:</template>
      </el-input>
    </div>
    <!-- <el-input
      placeholder="日志前n行将被处理，-1代表整个文档。默认为-1"
      v-model="dataObj.num"
      clearable>
    </el-input> -->
    <el-input
    placeholder="文件未上传"
    v-model="uploadtip"
    clearable>
    </el-input>
    <el-button
      type="success"
      plain
      :disabled="isdisabled"
      @click="watchAnalysis"
      >查看分析结果</el-button
    >
  </div>
</template>

<script>
export default {
  name: "SingleFileUpload",
  props: {
    value: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      isdisabled: false,
      uploadtip: "",
      scrfToken: "",
      dataObj: { name: "", num: "" },
    };
  },
  mounted: function () {
    //      this.getcsrftoken()
  },
  computed: {},
  methods: {
    getcsrftoken() {
      console.log("cookie:" + document.cookie);
    },

    beforeUpload(file) {
      this.uploadtip = "文件正在上传中。。。";
      this.dataObj["name"] = file.name;
    },

    uploadSuccess(response, file, fileList) {
      console.log("on-success");
      this.uploadtip = "文件已成功上传";
      if (response["error_num"] == 0) {
        this.isdisabled = false;
        // this.uploadtip = '文件已成功上传,并分析完成。'
      } else {
        this.uploadtip = "文件未成功上传，请稍后重试。";
      }
      //       for (var item in response) {
      //         console.log(item + '=' + response[item]);
      //       }
    },
    watchAnalysis() {
      console.log("查看分析结果");
      this.$router.push({ name: "Operate", query: { id: this.isdisabled } });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "~@/styles/mixin.scss";
.upload-container {
  width: 100%;
  position: relative;
  @include clearfix;
  .file-uploader {
    width: 100%;
    float: left;
  }
}
</style>
