<template>
  <el-table ref="multipleTable" :data="collect_table"
            style="margin: 0 auto;line-height:36px;font-size: 16px; text-align: center; width: 100%"
            @selection-change="handleSelectionChange">
    <el-table-column type="selection"/>
    <el-table-column property="CollectID" label="收集序号"/>
    <el-table-column property="CollectName" label="收集表名"/>
    <el-table-column property="FileType" label="收集类型"/>
    <el-table-column property="RenameStatus" label="是否重命名"/>
    <el-table-column property="RenameModels" label="重命名模板"/>
    <el-table-column property="CollectStartTime" label="收集开始时间"/>
    <el-table-column property="CollectEndTime" label="收集结束时间"/>
    <el-table-column label="基础权限操作">
      <template #default="scope">

        <el-button size="small" style="font-size: 16px" type="primary"
                   @click="collectDetails(scope.row['CollectID'])">详情
        </el-button>
        <el-button size="small" style="font-size: 16px" type="success" @click="copy_rusult(scope.row['CollectID'])">
          链接
        </el-button>

      </template>
    </el-table-column>
    <el-table-column label="高级权限操作">
      <template #default="scope">
        <el-button size="small" style="font-size: 16px" type="warning" @click="collectEdit(scope.row['CollectID'])">编辑
        </el-button>
        <el-button size="small" style="font-size: 16px" type="danger" @click="deleteSingin(scope.row['CollectID'])">
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import axios from 'axios'
import useClipboard from "vue-clipboard3";

const {toClipboard} = useClipboard();
export default {
  name: "Collect_CollectForm",
  data() {
    return {
      collect_table: [],
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
      axios.get("/api/collectfile/collecttable").then(res => {
        if (res.data['status'] === 200) {
          this.collect_table = res.data['collect_table']
        } else {
          this.$message.error('签到表查询错误' + res.data['status_context'])
        }
      })
    },

    collectEdit(CollectID) {
      this.$router.push({path: "/admin/collectfile/TableInfo", query: {'CollectID': CollectID}})

    },
    collectDetails(CollectID) {
      this.$router.push({path: '/admin/collectfile/TableDetails', query: {'CollectID': CollectID}})
    },
    deleteSingin(CollectID) {
      this.$confirm('是否删除收集表' + CollectID + '？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        axios.delete("/api/collectfile/collecttable", {'data': {'CollectID': CollectID}}).then(res => {
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
    copy_rusult(CollectID) {
      toClipboard(window.location.origin + '/student/#/student/collectfile?collect_id=' + CollectID);
      this.$message({message: '复制成功', type: 'success'})
    },
  }
}
</script>

<style scoped>

</style>