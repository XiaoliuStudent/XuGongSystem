<template>
  <!--  签到表单的管理-->
  <div style="background-color: #646cff; margin: 0 auto;text-align: left">
    <a-space style="">
      <router-link to="/admin/singin/" style="font-size: 22px;color: white;margin-left: 60px">首页</router-link>
      <el-divider direction="vertical"></el-divider>
      <router-link to="/admin/singin/CreateSingin" style="font-size:22px;color: white">新建签到表单</router-link>
      <p/>
    </a-space>
  </div>
  <router-view/>
</template>

<script>
export default {
  name: "SingIn",
  data() {
    return {
      singin_tables: []
    }
  }

}
</script>

<style scoped>

</style>