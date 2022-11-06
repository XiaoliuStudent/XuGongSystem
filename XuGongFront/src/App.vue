<template>
  <a-layout has-sider style="margin: 0 auto;text-align: center; background: white">
    <a-layout-sider collapsible
                    :style="{ overflow: 'auto', height: '100%', position: 'fixed', left: 0, top: 0, bottom: 0,}"
                    style="width: 100px"
    >
      <div class="logo"/>
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
        <a-menu-item>
          <router-link to="/">20计转本</router-link>
        </a-menu-item>
        <a-menu-item key="1">
          <user-outlined/>
          <span class="nav-text">
            <router-link to="/admin/hesuan/" type="primary" style="color: #f9f9f9">核酸管理</router-link>
          </span>
        </a-menu-item>
        <a-menu-item key="2">
          <video-camera-outlined/>
          <span class="nav-text">
           <router-link to="/admin/wechatclock/" type="primary" style="color: #f9f9f9">每日上报</router-link>
          </span>
        </a-menu-item>
        <a-menu-item key="3">
          <cloud-outlined/>
          <span class="nav-text">
            <router-link to="/admin/singin/" type="primary" style="color: #f9f9f9">签到管理</router-link>
          </span>
        </a-menu-item>
        <a-menu-item key="5">
          <upload-outlined/>
          <span class="nav-text">
            <router-link to="/admin/collectfile/" type="primary" style="color: #f9f9f9">文件收集</router-link>
          </span>
        </a-menu-item>
        <a-menu-item key="6">
          <bar-chart-outlined/>
          <span class="nav-text">
            <router-link to="/admin/docsheet/" type="primary" style="color: #f9f9f9">电子表格</router-link>
          </span>
        </a-menu-item>
        <a-menu-item key="7">
          <bar-chart-outlined/>
          <span class="nav-text">
            <router-link to="/admin/wordsearch/" type="primary" style="color: #f9f9f9">名单检索</router-link>
          </span>
        </a-menu-item>
        <a-menu-item key="8">
          <bar-chart-outlined/>
          <span class="nav-text">
            <a href="/student/" type="primary" style="color: #f9f9f9">学生系统</a>
          </span>
        </a-menu-item>


      </a-menu>
    </a-layout-sider>
    <a-layout :style="{ marginLeft: '200px', width: '800px' }">
      <div style="width: 100%; margin: 0 auto;text-align: center; background: #ffffff">


        <div :style="{ padding: '24px', background: '#ffffff', margin: '0 auto'}">
          <div style="width: max-content;  margin: 0 auto; text-align: center">
            <h2 style=" color:#646cff;font-family: '微软雅黑'; font-size: 36px; font-weight: bold;">20计转本
              班级日常事务管理系统</h2></div>
        </div>


        <a-layout-content :style="{ overflow  : 'initial' , width: '100%'}">
          <router-view/>
        </a-layout-content>


        <div :style="{ padding: '24px', background: '#ffffff', margin: '0 auto', width: '100%'}">
          <router-link to="/admin/about" style="width: 100%;  margin: 0 auto; text-align: center; color: #b1b3b8">
            20计转本 班级日常事务管理系统 2022 Created by 秋后的奶茶队.
          </router-link>
        </div>
      </div>
    </a-layout>

  </a-layout>

</template>


<script lang="ts">
import {
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  BarChartOutlined,
  CloudOutlined,
  AppstoreOutlined,
  TeamOutlined,
  ShopOutlined,
} from '@ant-design/icons-vue';
import {defineComponent, ref} from 'vue';
import {useStore} from 'vuex'

export default defineComponent({
  components: {
    UserOutlined,
    VideoCameraOutlined,
    UploadOutlined,
    BarChartOutlined,
    CloudOutlined,
    AppstoreOutlined,
    TeamOutlined,
    ShopOutlined,
  },
  setup() {
    return {
      selectedKeys: ref<string[]>(['4']),
    };
  },
  data() {
    return {
      selectedKeys: 1
    }
  }
});

</script>


<style>
#components-layout-demo-fixed-sider .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px;
}

.site-layout .site-layout-background {
  background: #fff;
}

[data-theme='dark'] .site-layout .site-layout-background {
  background: #141414;
}
</style>
