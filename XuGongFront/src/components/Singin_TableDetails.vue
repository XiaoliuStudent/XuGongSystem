<template>
  <div>
    <el-progress :text-inside="true" :stroke-width="24" :percentage="percentage" style="width: 1500px; margin: 0 auto;"
                 status="success" stroke-linecap="butt" :format="compute_percentage"/>

    <el-table ref="multipleTable" :data="singin_students"
              style="margin: 0 auto; width:1500px;line-height:36px;font-size: 16px; text-align: center"
              @selection-change="handleSelectionChange">
      <el-table-column type="selection"/>
      <el-table-column property="SinginID" label="签到表序号"/>
      <el-table-column property="SinginName" label="签到表名"/>
      <el-table-column property="SinginType" label="签到类型"/>
      <el-table-column property="StudentID" label="学号"/>
      <el-table-column property="StudentName" label="姓名"/>

      <el-table-column property="SinginStatus" label="签到状态" style="width: 66px;" :filters="[
        { text: '已签到', value: '已签到' },
        { text: '未签到', value: '未签到' },
      ]" :filter-method="filterTag" filter-placement="bottom-end">
        <template #default="scope">
          <el-tag :type="scope.row.SinginStatus==='已签到'?'':'success'" disable-transitions
                  style="height: 36px;font-size: 16px">
            {{ scope.row.SinginStatus }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column property="SinginTime" label="签到时间"/>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="PostSingin(scope.row['StudentID'])">签到</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "Singin_TableInfo",
  data() {
    return {
      SinginID: '',
      singin_students: [],
      percentage: 80,
      singin_success_size: 0,
      singin_error_size: 0
    }
  },
  mounted() {
    this.SinginID = this.$route.query.SinginID
    this.GetSinginDetails()
  },
  methods: {
    compute_percentage() {
      this.percentage = Math.round(this.singin_success_size / (this.singin_success_size + this.singin_error_size) * 100)
      return "已签到：" + this.singin_success_size + "人，未签到：" + this.singin_error_size + "人，签到率：" + this.percentage + "%"
    },
    GetSinginDetails() {
      axios.get("/api/singin/student/singin", {'params': {'SinginID': this.SinginID}}).then(res => {
        this.singin_students = res.data['SinginDetails']['students']
        this.singin_success_size = res.data['SinginDetails']['singin_size_info']['singin_success_size']
        this.singin_error_size = res.data['SinginDetails']['singin_size_info']['singin_error_size']
      })
    },
    PostSingin(StudentID) {
      axios.post("/api/singin/student/singin", {"student_id": StudentID, "singin_id": this.SinginID}).then(
          res => {
            if (res.data['status'] === 200) {
              this.singin_status = "success"
              this.$message({message: "签到成功", type: "success"})
              this.GetSinginDetails()
            } else {
              this.$message.error(res.data['status_context'])
            }
          }
      )

    },
    filterTag(value, row) {
      return row.SinginStatus === value
    }
  }
}
</script>
<style scoped>

</style>