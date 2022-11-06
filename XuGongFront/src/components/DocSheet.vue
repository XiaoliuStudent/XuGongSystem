<template>
  <div style="margin: 0 auto;  text-align: center">
    <el-table :data="students" style="width: 100%">
      <el-table-column type="selection" width="55"/>
      <el-table-column prop="ID" label="学号"/>
      <el-table-column prop="Class" label="班级"/>
      <el-table-column prop="Name" label="姓名"/>
      <el-table-column prop="IDCard" label="身份证号"/>
      <el-table-column prop="Gender" label="性别"/>
      <el-table-column prop="Phone" label="电话"/>
      <el-table-column prop="QQID" label="QQ"/>
      <el-table-column prop="Dorm" label="宿舍"/>
      <el-table-column prop="Comment" label="备注">
        <template #default="scope">
          <el-input v-model="scope.row.Comment" placeholder=""/>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import UserList from "./UserList.vue";
import {getCurrentInstance} from "vue";
import axios from "axios";

export default {
  name: "docsheet",
  data() {
    return {
      students: [],
    }
  },
  //请求学生数据
  mounted() {
    axios.get("/api/docsheet/students").then(res => this.students = res.data['students'])
  }


}
</script>

<style scoped>

</style>