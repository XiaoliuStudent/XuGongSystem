<template>
  <el-table ref="multipleTable" :data="singin_tables"
            style="margin: 0 auto;line-height:36px;font-size: 16px; text-align: center; width: 100%"
            @selection-change="handleSelectionChange">
    <el-table-column type="selection"/>
    <el-table-column property="SinginID" label="签到序号"/>
    <el-table-column property="SinginName" label="签到表名"/>
    <el-table-column property="SinginType" label="签到类型"/>
    <el-table-column property="SinginStartTime"  label="签到开始时间"/>
    <el-table-column property="SinginEndTime" label="签到结束时间"/>
    <el-table-column label="基础权限操作" >
      <template #default="scope">

          <el-button size="small" style="font-size: 16px" type="primary" @click="SinginTableDetails(scope.row['SinginID'])">详情</el-button>
          <el-button size="small" style="font-size: 16px" type="success" @click="copy_rusule(scope.row['SinginID'])">链接</el-button>

      </template>
    </el-table-column>
    <el-table-column label="高级权限操作">
      <template #default="scope">
        <el-button size="small" style="font-size: 16px" type="warning" @click="singinInfo(scope.row['SinginID'])">编辑</el-button>
        <el-button size="small" style="font-size: 16px" type="danger" @click="deleteSingin(scope.row['SinginID'])">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import axios from 'axios'
import useClipboard from "vue-clipboard3";

const {toClipboard} = useClipboard();
export default {
  name: "Singin_SinginTable",
  data() {
    return {
      singin_tables: [],
    }
  },

  // 获取全部的签到表
  mounted() {
    setTimeout(() => {
    }, 3000)
    this.getTable()
  },
  methods: {
    getTable() {
      axios.get("/api/singin/singintable").then(res => {
        if (res.data['status'] === 200) {
          this.singin_tables = res.data['singin_tables']
        } else {
          this.$message.error('签到表查询错误' + res.data['status_context'])
        }
      })
    },
    singinInfo(SinginID) {
      this.$router.push({path: "/admin/singin/TableInfo", query: {'SinginID': SinginID}})

    },
    SinginTableDetails(SinginID) {
      this.$router.push({path: '/admin/singin/TableDetails', query: {'SinginID': SinginID}})
    },
    deleteSingin(SinginID) {
      this.$confirm('是否删除签到表' + SinginID + '？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        axios.delete("/api/singin/singintable", {'data': {'SinginID': SinginID}}).then(res => {
          if (res.data['status'] === 200) {
            this.$message({message: res.data['status_context'], type: 'success'})
            this.getTable()
          } else {
            this.$message.error('删除签到表错误' + res.data['status_conetxt'])
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消发送'
        });
      })
    },
    copy_rusule(SinginID) {
      toClipboard(window.location.origin + '/student/#/student/singin?singin_id=' + SinginID);
      this.$message({message: '复制成功', type: 'success'})
    },
  }
}
</script>

<style scoped>

</style>