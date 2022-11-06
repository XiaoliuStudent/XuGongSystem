<template>
  <!--  <div style="width: 100%;  margin: 0 auto; text-align: center">-->
  <!--    <h2 style=" color:#646cff;font-family: '微软雅黑'; font-size: 32px; font-weight: bold;">20计转本 文件收集</h2>-->
  <!--  </div>-->

  <div>
    <el-form ref="formRef" :model="student_id" class="demo-ruleForm">
      <el-form-item label="学号" :rules="[
        { required: true, message: '请输入学号' },
        { type: 'number', message: '请输入完整的学号' }]">
        <el-input v-model="student_id" type="text" autocomplete="off" placeholder="请输入学号"/>
      </el-form-item>
    </el-form>
  </div>


  <div>
    <el-upload
        class="upload-demo"
        drag
        action="/api/collectfile/uploadfile"
        multiple
        :auto-upload="false"
        ref="uploadRef"
        :headers="{'collect-id':upload_id,'student-id':student_id}"
    >
      <el-icon class="el-icon--upload">
        <upload-filled/>
      </el-icon>
      <div class="el-upload__text">
        Drop file here or <em>click to upload</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
          目前只支持上传单文件
        </div>
      </template>
    </el-upload>
    <el-button @click="submitUpload">上传文件</el-button>


  </div>
</template>


<script lang="ts" setup>

import {ref} from 'vue'
import axios from 'axios';


import {UploadFilled} from '@element-plus/icons-vue'
import type {UploadInstance} from 'element-plus'

const uploadRef = ref<UploadInstance>()
const submitUpload = () => {
  uploadRef.value!.submit()
}

</script>

<script lang="ts">
export default {
  data() {
    return {
      student_id: null,
      upload_id: null,
      upload_status: "warning",
      upload_url: "/api/collectfile/uploadfile?upload_id="
    }
  },

  mounted() {
    this.upload_id = this.$route.query.collect_id;
    this.student_id = this.$route.query.student_id
    if (this.upload_id === undefined) {
      this.$message.error("文件收集网址参数错误")
    } else {
      this.upload_url = this.upload_url + this.upload_id
    }
    if (this.student_id === undefined) {
      this.student_id = ''
    } else {
    }
  },

  methods: {
    //   upload_file() {
    //     this.$confirm('是否上传文件？', '提示', {
    //       confirmButtonText: '确定',
    //       cancelButtonText: '取消',
    //       type: 'warning'
    //     }).then(() => {
    //       this.submitUpload()
    //     }).catch(() => {
    //       this.$message({
    //         type: 'info',
    //         message: '取消aaa上传'
    //       })
    //     })
    //   }
  }
}

</script>

<style scoped>

</style>