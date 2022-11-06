<template>
  <div style="width: 100%;  margin: 0 auto; text-align: center">
    <h2 style=" color:#646cff;font-family: '微软雅黑'; font-size: 32px; font-weight: bold;">20计转本 学生签到</h2>
  </div>

  <div>
    <el-form ref="formRef" :model="student_id" class="demo-ruleForm">
      <el-form-item label="学号" :rules="[
        { required: true, message: '请输入学号' },
        { type: 'number', message: '请输入完整的学号' }]">
        <el-input v-model="student_id" type="text" autocomplete="off" placeholder="请输入学号"/>
      </el-form-item>
    </el-form>
  </div>


  <div style="margin: 0 auto; width: 100%">
    <el-result :icon="singin_status">
      <template #extra>
        <el-button @click="post_singin" style="font-size: 22px; font-weight: bold" size="large" type="primary">签到
        </el-button>
      </template>
    </el-result>
  </div>
</template>


<script>
import axios from 'axios'
export default {
  name: "studentsingin",
  data() {
    return {
      student_id: null,
      singin_id: null,
      singin_status: "warning",
    }
  },
  mounted() {
    this.singin_id = this.$route.query.singin_id;
    if (this.singin_id === undefined) {
      this.$message.error("签到网址参数错误")
    } else {
    }
  },
  methods: {
    post_singin() {

      if (this.student_id !== null && this.student_id.length === 11 && this.student_id.includes('20090102')) {
        axios.post("/api/singin/student/singin", {"student_id": this.student_id, "singin_id": this.singin_id}).then(
            res => {
              if (res.data['status'] === 200) {
                this.singin_status = "success"
                this.$message({message: "签到成功", type: "success"})
              }else{
                this.$message.error(res.data['status_context'])
              }
            }
        )

      } else {
        this.$message.error("请输入正确的学号")
      }
    }
  }
}


</script>

<style scoped>

</style>