<template>
  <p/>
  <el-form ref="formRef" class="demo-ruleForm"
           style="width: 40%;margin: 0 auto; text-align: left">
    <el-form-item v-if="PostType==='Create'" label="文件收集表单ID：">
      <el-input v-model="CollectID" type="text" autocomplete="off" placeholder="请输入收集表单ID"/>
    </el-form-item>
    <el-form-item label="文件收集表单名字：">
      <el-input v-model="CollectName" type="text" autocomplete="off" placeholder="请输入收集表单名字"/>
    </el-form-item>

    <el-form-item label="文件收集类型：">
      <el-radio v-model="FileType" label="单文件收集">单文件收集</el-radio>
      <el-radio v-model="FileType" label="多文件收集">多文件收集</el-radio>
      <el-radio v-model="FileType" label="自定义收集类型">自定义收集类型</el-radio>
    </el-form-item>
    <el-form-item label="文件是否重命名">
      <el-radio v-model="RenameStatus" label="True">是</el-radio>
      <el-radio v-model="RenameStatus" label="False">否</el-radio>
    </el-form-item>
    <el-form-item v-if="RenameStatus==='True'" label="文件重命名模板：">
      <el-select v-model="RenameModels" multiple filterable allow-create default-first-option
                 placeholder="请选择重命名的项">
        <el-option
            v-for="item in Models_list" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>
    </el-form-item>

    <div class="block">
      <span class="demonstration">收集时间范围：</span>
      <el-date-picker
          v-model="CollectStartTime"
          type="datetime"
          placeholder="收集开始时间">
      </el-date-picker>
      <el-date-picker
          v-model="CollectEndTime"
          type="datetime"
          placeholder="收集结束时间">
      </el-date-picker>
    </div>

    <div v-if="showSinginInfoStatus === 1" style="margin: 0 auto; text-align: center; margin-top: 20px">

      <vue-qrcode :value="collect_file_url" :options="{ width: 200 }"></vue-qrcode>
      <p></p>
      <el-button type="primary" @click="copy_rusult" class="button0" style="height: 36px">{{
          collect_file_url
        }}
      </el-button>
    </div>

  </el-form>

  <div style="margin-top: 40px" v-if="status === true">
    <el-button type="success" @click="cancel_create" class="button0" style="height: 36px ;font-size: 16px">取消
    </el-button>
    <el-button type="primary" @click="create_form" class="button0" style="height: 36px ">创建收集</el-button>
  </div>

</template>

<script>
import axios from "axios";
import useClipboard from "vue-clipboard3";


const {toClipboard} = useClipboard();

export default {
  name: "Singin_CreateSingin",

  data() {
    return {
      CollectID: '',
      CollectName: '',
      FileType: '',
      CollectStartTime: '',
      CollectEndTime: '',
      PostType: 'Create',
      showSinginInfoStatus: 0,
      collect_file_url: '点击复制表单地址',
      status: true,
      rename_models_comment: "",

      RenameStatus: '',
      Models_list: [
        {
          value: '学号',
          label: '学号'
        },
        {
          value: '班级',
          label: '班级'
        },
        {
          value: '姓名',
          label: '姓名'
        },
        {
          value: '身份证号',
          label: '身份证号'
        },
        {
          value: '手机号码',
          label: '手机号码'
        },
        {
          value: '宿舍',
          label: '宿舍'
        },
        {
          value: '两位学号',
          label: '两位学号'
        },
        {
          value: '_',
          label: '_'
        },
        {
          value: '-',
          label: '-'
        }],
      RenameModels: []
    }
  },
  mounted() {
    this.CollectID = this.$route.query.CollectID
    if (this.CollectID !== undefined) {
      this.get_form(this.CollectID)
      this.PostType = 'Update'
    }
  },
  methods: {
    create_form() {
      this.$confirm('是否创建收集表单？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        axios.post("/api/collectfile/collecttable", {
          'CollectID': this.CollectID,
          'CollectName': this.CollectName,
          'FileType': this.FileType,
          'RenameStatus': this.RenameStatus,
          'RenameModels': this.RenameModels,
          'CollectStartTime': this.CollectStartTime,
          'CollectEndTime': this.CollectEndTime,
          'PostType': this.PostType
        }).then(res => {
          if (res.data['status'] === 200) {
            this.$message({message: res.data['status_context'], type: 'success'})

            //  下一步操作，展示数据
            if (this.PostType === "Update") {
              this.$router.push({path: '/admin/collectfile/'})
            } else {
              this.show_create_result(res.data)
            }
            this.status = false
          } else {
            this.$message.error('新建表单失败' + res.data['status_conetxt'])
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消创建'
        });
      })
    },
    show_create_result(data) {
      this.showSinginInfoStatus = 1
      this.collect_file_url = window.location.origin + data['CollectInfo']['CollectUrl']
    },
    cancel_create() {
      this.$message({
        type: 'info',
        message: '取消创建'
      })
      this.$router.push({path: "/admin/collectfile/"})
    },
    get_form(CollectID) {
      axios.get("/api/collectfile/collecttable", {'params': {'CollectID': CollectID}}).then(res => {
        if (res.data['status'] === 200) {
          this.CollectID = res.data['collect_table'][0]['CollectID']
          this.CollectName = res.data['collect_table'][0]['CollectName']
          this.FileType = res.data['collect_table'][0]['FileType']
          this.RenameStatus = res.data['collect_table'][0]['RenameStatus']
          this.RenameModels = res.data['collect_table'][0]['RenameModels']
          this.CollectStartTime = res.data['collect_table'][0]['CollectStartTime']
          this.CollectEndTime = res.data['collect_table'][0]['CollectEndTime']

        } else {
          this.$message.error('文件收集表单查询错误' + res.data['status_context'])
        }
      })
    },
    copy_rusult() {
      toClipboard(this.collect_file_url);
      this.$message({message: '复制成功', type: 'success'})
    },
  }
}
</script>

<style scoped>

</style>