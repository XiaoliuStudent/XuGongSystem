<template>
  <div>
    <div>
      <el-progress :text-inside="true" :stroke-width="24" :percentage="percentage"
                   style="width: 1500px; margin: 0 auto"
                   status="success" stroke-linecap="butt" :format="compute_percentage" color="#646cff"/>
      <div style="margin-left: 10px">
        <el-button style="left: auto">
          <a :href="'/api/collectfile/managefile?CollectID='+this.CollectID">下载所有文件</a>
        </el-button>
        <el-button @click="delete_allfiles">删除所有文件</el-button>
        <el-button @click="CollectDetails">刷新数据</el-button>
      </div>
    </div>


    <el-table ref="multipleTable" :data="collect_students"
              style="margin: 0 auto; width:1500px;line-height:36px;font-size: 16px; text-align: center"
              @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"/>
      <el-table-column property="CollectID" width="100" label="单号"/>
      <el-table-column property="CollectName" label="收集表单序名"/>
      <el-table-column property="StudentID" label="学号"/>
      <el-table-column property="StudentName" label="姓名"/>

      <el-table-column property="UploadStatus" label="上传状态" style="width: 66px;" :filters="[
        { text: '已上传', value: '已上传' },
        { text: '未上传', value: '未上传' },
      ]" :filter-method="filterTag" filter-placement="bottom-end">
        <template #default="scope">
          <el-tag :type="scope.row.UploadStatus==='已上传'?'':'success'" disable-transitions
                  style="height: 36px;font-size: 16px">
            {{ scope.row.UploadStatus }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column property="UploadFileNames" label="上传文件名"/>
      <el-table-column property="UploadTime" label="上传时间"/>
      <el-table-column label="操作文件">
        <template #default="scope">
          <el-button size="small">
            <a :href="'/student/#/student/collectfile?collect_id='+this.CollectID+'&student_id='+scope.row['StudentID']"
               target="_blank">上传</a>
          </el-button>
          <el-button size="small" @click="download_file(this.CollectID,scope.row['UploadFileNames'])">
            <a :href="'/files/student_collectfiles/'+this.CollectID + '/' + scope.row['UploadFileNames']" download=""
               target="_blank">下载</a>
          </el-button>
          <el-button size="small" @click="delete_file(scope.row['StudentID'],scope.row['UploadFileNames'])">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "Collect_TableDetails",
  data() {
    return {
      CollectID: '',
      collect_students: [],
      percentage: 80,
      collect_success_size: 0,
      collect_error_size: 0
    }
  },
  mounted() {
    this.CollectID = this.$route.query.CollectID
    this.CollectDetails()
  },
  methods: {
    compute_percentage() {
      this.percentage = Math.round(this.collect_success_size / (this.collect_success_size + this.collect_error_size) * 100)
      return "已上传：" + this.collect_success_size + "人，未上传：" + this.collect_error_size + "人，上传率：" + this.percentage + "%"
    },
    CollectDetails() {
      axios.get("/api/collectfile/uploadfile", {'params': {'CollectID': this.CollectID}}).then(res => {
        this.collect_students = res.data['CollectDetails']['students']
        this.collect_success_size = res.data['CollectDetails']['collect_size_info']['collect_success_size']
        this.collect_error_size = res.data['CollectDetails']['collect_size_info']['collect_error_size']
      })
    },
    download_allfiles() {
      axios.get("/api/collectfile/managefile", {params: {'CollectID': this.CollectID}})
    },
    delete_allfiles() {
      this.$confirm('是否删除所有同学文件', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        axios.delete("/api/collectfile/managefile", {
          'data': {
            "CollectID": this.CollectID
          }
        }).then(res => {
          if (res.data['status'] === 200) {
            this.$message({message: res.data['status_context'], type: 'success'})
            this.CollectDetails()
          } else {
            this.$message.error("删除失败", res.data['status_context'])
          }
        })

      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消删除'
        })
      })
    },

    delete_file(student_id, file_name) {
      this.$confirm('是否删除已上传的文件', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        axios.delete("/api/collectfile/uploadfile", {
          'data': {
            "CollectID": this.CollectID,
            "file_name": file_name,
            "StudentID": student_id
          }
        }).then(res => {
          if (res.data['status'] === 200) {
            this.$message({message: res.data['status_context'], type: 'success'})
            this.CollectDetails()
          } else {
            this.$message.error("删除失败", res.data['status_context'])
          }
        })

      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消删除'
        })
      })
    },
    filterTag(value, row) {
      return row.UploadStatus === value
    }

  }
}
</script>
<style scoped>

</style>