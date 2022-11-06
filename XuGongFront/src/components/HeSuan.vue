<template>
  <div id="main" v-loading="fullscreenLoading">
    <!--定义头部-->
    <div id="docInfo" style="width: 100%; margin: 0 auto">
      <a-space>
        <el-input v-model="doc_url" :placeholder="doc_title_info" class="button1"
                  style="width: 560px; height: 40px"></el-input>
        <el-button type="primary" @click="send_url" class="button0" style="height: 40px">提交文档地址</el-button>
      </a-space>
    </div>
    <p></p>


    <div id="MainTable">
      <el-progress :percentage="percentage"
                   style="width:700px; margin: 0 auto;"
                   status="success" stroke-linecap="butt"/>
      <el-table ref="multipleTable" :data="students"
                style="width:700px; margin: 0 auto;line-height:36px;font-size: 16px"
                @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" style="width: 100%;"/>
        <el-table-column property="xuehao" label="学号" style="width: 66px;"/>
        <el-table-column property="class" label="班级" style="width: 66px;"/>
        <el-table-column property="name" label="姓名" style="width: 66px;"/>

        <el-table-column property="status" label="是否完成核酸" style="width: 66px;" :filters="[
        { text: '已完成', value: '已完成' },
        { text: '未完成', value: '未完成' },
      ]" :filter-method="filterTag" filter-placement="bottom-end">
          <template #default="scope">
            <el-tag :type="scope.row.status==='已完成'?'':'success'" disable-transitions
                    style="height: 36px;font-size: 16px">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      <div style="margin-top: 30px">
        <el-button @click="toggleSelection(students)">一键选择未打卡记录</el-button>
        <el-button @click="toggleSelection()">清除所勾选的记录</el-button>
      </div>
    </div>

    <!--定义底部按钮-->
    <div id="post_mail" style="margin-top: 40px">
      <el-button type="primary" @click="copy_rusule" class="button0" style="height: 36px">{{
          clock_resule
        }}
      </el-button>
      <el-button type="warning" @click="open_doc" class="button0" style="height: 36px">
        <a v-bind:href="doc_open_url" target="_blank" style="color: white">打开腾讯文档</a>
      </el-button>
      <el-button type="success" @click="post_mail" class="button0" style="height: 36px">发送邮件提醒</el-button>
    </div>
  </div>


</template>

<script>
import useClipboard from "vue-clipboard3";
import axios from "axios"
import UserList from "./UserList.vue";

const {toClipboard} = useClipboard();
// interface Student {
//   xuehao: string
//   class: string
//   name: string
//   status: string
// }
export default {
  name: "HeSuan",
  components: {UserList},
  data() {
    return {
      doc_url: '',
      doc_title: '',
      doc_title_info: '请输入腾讯文档地址',
      doc_open_url: '',

      students: [],
      send_object: [],

      clock_resule: "点击进行复制",
      fullscreenLoading: false,
      percentage: 80
    }
  },
  // response.data['history_doc_title'] !== null ? this.doc_title = response.data['history_doc_title'] : this.doc_title = "请输入腾讯文档地址",
  //     this.doc_url = response.data['history_doc_url']
  mounted() {
    axios.get("/api/hesuan/historydoc").then(
        response => {
          if (response.data['history_doc_title'] !== null) {
            this.doc_open_url = response.data['history_doc_url']
            this.doc_url = response.data['history_doc_title'] + response.data['history_doc_url']
            this.doc_title = response.data['history_doc_title'] + response.data['history_doc_url']
          } else {
          }
        }
    )
    setTimeout(() => {
      this.percentage = 0
    }, 200)
  },

  methods: {
    send_url() {
      if (this.doc_url.includes('sheet')) {
        this.fullscreenLoading = true;
        axios.get("/api/hesuan/userlist?class_name=20计转本&doc_url=" + this.doc_url).then(
            response => {
              this.clock_resule = '20计转本应做' + (response.data['count_size']['true_size'] + response.data['count_size']['false_size']) + '人，已做' + response.data['count_size']['true_size'] + '人'
              this.students = response.data['students']
              this.fullscreenLoading = false
              this.percentage = Math.round(response.data['count_size']['true_size'] / (response.data['count_size']['true_size'] + response.data['count_size']['false_size']) * 100)

            }
        )
      } else (
          this.$message({message: '腾讯文档地址输入错误，请重新输入！', type: 'error'})
      )
    },

    copy_rusule() {
      toClipboard(this.clock_resule);
      this.$message({message: '复制成功', type: 'success'})
    },

    post_mail() {
      this.send_object = []
      this.students.forEach(row => {
            if (row['send'] === true) {
              this.send_object.push(row['xuehao'])
            } else {
            }
          }
      );
      this.$confirm('将发送邮件给以下同学：' + this.send_object, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.fullscreenLoading = true
        axios.post("/api/hesuan/sendmail", {'objects': this.send_object}).then(res => {
          if (res.data['status'] === 200) {
            this.$message({message: res.data['status_context'] + res.data['persient_list'], type: 'success'})
          } else {
            this.$message.error(res.data['status_context'])
          }
          this.fullscreenLoading = false
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消发送'
        });
      });
    },
    test_print_student() {
      console.log(this.students)
    },


    toggleSelection(rows) {
      if (rows) {
        rows.forEach(row => {
          if (row['status'] === '未完成') {
            this.$refs.multipleTable.toggleRowSelection(row)
          } else {
          }
        });
      } else {
        this.students.forEach(row => (row['send'] = false))
        this.$refs.multipleTable.clearSelection();
      }
    },
    handleSelectionChange(rows) {
      this.students.forEach(row => (row['send'] = false))

      if (rows) {
        rows.forEach(row => {
          // 定义选择发送对象
          row['send'] = true
        })
      } else {
      }

    },

    filterTag(value, row) {
      return row.status === value
    }
  }

}

</script>

<style scoped>

</style>