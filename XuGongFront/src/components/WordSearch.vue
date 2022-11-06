<template>
  <div>

    <div style="width: 60%; margin: 0 auto">
      <el-input style="width:80%"
                type="textarea"
                :rows="4"
                placeholder="请复制粘贴姓名学号"
                v-model="textarea">
      </el-input>


      <div style="width: 100px; float: right">
        <el-button style="font-size: 20px; height: 48px;" class="button0"
                   @click="PostTextarea" type="primary">发送检索
        </el-button>
        <!--                  <el-divider direction="vertical"></el-divider>-->
        <p></p>
        <div style="background-color:#409eff ; width: 111px; float: left; ">
          <input ref="file" style="float: left;width: 72px" type='file'
                 name="file" webkitdirectory @change.stop="PostFiles"/>
        </div>


      </div>
    </div>


    <div v-if="result_status === true">
      <el-table ref="multipleTable" :data="students"
                style="width:70%; margin: 0 auto;line-height:36px;font-size: 16px"
                @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" style="width: 100%;"/>
        <el-table-column property="ID" label="学号" style="width: 66px;"/>
        <el-table-column property="Name" label="姓名" style="width: 66px;"/>
        <el-table-column property="SearchStatus" label="检索结果" style="width: 66px;" :filters="[
        { text: 'True', value: 'True' },
        { text: 'False', value: 'False' },
      ]" :filter-method="filterTag" filter-placement="bottom-end">
          <template #default="scope">
            <el-tag :type="scope.row.SearchStatus==='True'?'':'success'" disable-transitions
                    style="height: 36px;font-size: 16px">
              {{ scope.row.SearchStatus }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>


</template>

<script>
import axios from 'axios'

axios;
export default {
  name: "WordSearch",
  data() {
    return {
      textarea: '',
      result_status: false,
      files: [],
    }
  },
  methods: {
    PostTextarea() {
      this.$confirm('是否继续发送文字域？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let post_data = {'type': 'textarea', 'textarea': this.textarea};
        this.post_search(post_data)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消发送'
        });
      })
    },
    post_search(post_data) {
      axios.post("/api/wordsearch/wordsearch", post_data).then(res => {
        if (res.data['status'] === 200) {
          this.result_status = true
          this.students = res.data['search_result']
          //  正确内容放置
        } else {
          // 错误内容放置
          this.$message.error('检索失败' + res.data['status_conetxt'])
        }
      })
    },
    filterTag(value, row) {
      return row.SearchStatus === value
    },
    PostFiles() {
      let post_data = {'type': 'files', 'files': []}
      console.log(post_data)
      for (let i = 0; i < this.$refs.file.files.length; i++) {
        post_data['files'].push(this.$refs.file.files.item(i)['name'])
      }
      this.post_search(post_data)
    }

  }
}
</script>

<style scoped>

</style>