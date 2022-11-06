<template>
  <p/>
  <el-form ref="formRef" :model="student_id" class="demo-ruleForm"
           style="width: 40%;margin: 0 auto; text-align: left">
    <el-form-item label="签到表单ID：" rules="[{ required: true}]">
      <el-input v-model="SinginID" type="text" autocomplete="off" placeholder="请输入签到表单ID"/>
    </el-form-item>
    <el-form-item label="签到表单名字：" rules="[{ required: true}]">
      <el-input v-model="SinginName" type="text" autocomplete="off" placeholder="请输入签到表单名字"/>
    </el-form-item>
    <el-form-item label="签到类型：" rules="[{ required: true}]">
      <el-radio v-model="SinginType" label="全员签到">全员签到</el-radio>
      <el-radio v-model="SinginType" label="宿舍签到">宿舍签到</el-radio>
      <el-radio v-model="SinginType" label="自定义人员签到">自定义人员签到</el-radio>
    </el-form-item>

    <div class="block">
      <span class="demonstration">签到时间范围：</span>
      <el-date-picker
          v-model="SinginStartTime"
          type="datetime"
          placeholder="签到开始时间">
      </el-date-picker>
      <el-date-picker
          v-model="SinginEndTime"
          type="datetime"
          placeholder="签到结束时间">
      </el-date-picker>
    </div>

    <div v-if="showSinginInfoStatus === 1" style="margin: 0 auto; text-align: center; margin-top: 20px">

      <vue-qrcode :value="SinginUrl" :options="{ width: 200 }"></vue-qrcode>
      <p></p>
      <el-button type="primary" @click="copy_rusule" class="button0" style="height: 36px">{{
          SinginUrl
        }}
      </el-button>
    </div>

  </el-form>

  <div style="margin-top: 40px" v-if="status === true">
    <el-button type="success" @click="cancel_create" class="button0" style="height: 36px ;font-size: 16px">取消
    </el-button>
    <el-button type="primary" @click="create_singin" class="button0" style="height: 36px ">创建签到</el-button>
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
      SinginID: '',
      SinginName: '',
      SinginType: '全员签到',
      SinginStartTime: '',
      SinginEndTime: '',
      PostType: 'Create',
      showSinginInfoStatus: 0,
      SinginUrl: '点击复制签到地址',
      status: true
    }
  },
  mounted() {
    this.SinginID = this.$route.query.SinginID
    if (this.SinginID !== undefined) {
      this.getTable(this.SinginID)
      this.PostType = 'Update'
    }
  },
  methods: {
    create_singin() {
      this.$confirm('是否创建签到？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        axios.post("/api/singin/singintable", {
          'SinginID': this.SinginID,
          'SinginName': this.SinginName,
          'SinginType': this.SinginType,
          'SinginStartTime': this.SinginStartTime,
          'SinginEndTime': this.SinginEndTime,
          'PostType': this.PostType
        }).then(res => {
          if (res.data['status'] === 200) {
            this.$message({message: res.data['status_context'], type: 'success'})

            //  下一步操作，展示数据
            if (this.PostType === "Update") {
              this.$router.push({path: '/admin/singin/'})
            } else {
              this.showSinginInfo(res.data)
            }
            this.status = false
          } else {
            this.$message.error('新建签到失败' + res.data['status_conetxt'])
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消创建'
        });
      })
    },
    showSinginInfo(data) {
      this.showSinginInfoStatus = 1
      this.SinginUrl = window.location.origin+data['SinginInfo']['SinginUrl']
    },
    cancel_create() {
      this.$message({
        type: 'info',
        message: '取消创建'
      })
      this.$router.push({path: "/admin/singin/"})
    },
    getTable(SinginID) {
      axios.get("/api/singin/singintable", {'params': {'SinginID': SinginID}}).then(res => {
        if (res.data['status'] === 200) {
          this.SinginID = res.data['singin_tables'][0]['SinginID']
          this.SinginName = res.data['singin_tables'][0]['SinginName']
          this.SinginType = res.data['singin_tables'][0]['SinginType']
          this.SinginStartTime = res.data['singin_tables'][0]['SinginStartTime']
          this.SinginEndTime = res.data['singin_tables'][0]['SinginEndTime']

        } else {
          this.$message.error('签到表查询错误' + res.data['status_context'])
        }
      })
    },
    copy_rusule() {
      toClipboard(this.SinginUrl);
      this.$message({message: '复制成功', type: 'success'})
    },
  }
}
</script>

<style scoped>

</style>