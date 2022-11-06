<template>
  <!--  签到表单的管理-->
  <div style="background-color: #67c23a; margin: 0 auto;text-align: left">
    <a-space style="">
      <router-link to="/admin/collectfile/" style="font-size: 22px;color: white;margin-left: 60px">首页</router-link>
      <el-divider direction="vertical"></el-divider>
      <router-link to="/admin/collectfile/CreateCollect" style="font-size:22px;color: white">新建收集表单</router-link>
      <p/>
    </a-space>
  </div>
  <router-view/>
</template>

<script>
export default {
  name: "CollectFile",
  data() {
    return {
    }
  }

}
</script>

<style scoped>

</style>