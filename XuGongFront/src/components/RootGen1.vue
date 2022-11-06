<template>
  <el-image style="width: 60%; height: 60%; margin-top: 0px"
            src="/public/IndexMain.png" fit="contain"/>
  <p/>
  <h2>20计转本 班级日常事务管理系统 正在开发中</h2>

  <el-progress :text-inside="true" :stroke-width="24" :percentage="percentage" style="width: 80%; margin: 0 auto;" status="success"/>
</template>

<script>
export default {
  name: "RootGen1",
  data() {
    return {
      percentage: 0
    }
  },
  mounted() {
    setTimeout(()=>this.percentage = 98, 200)
  }
}
</script>

<style scoped>
.demo-image .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 20%;
  box-sizing: border-box;
  vertical-align: top;
}

.demo-image .block:last-child {
  border-right: none;
}

.demo-image .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>