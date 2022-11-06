<script>
import {createRouter, createWebHashHistory} from 'vue-router';
import DocSheet from "../components/DocSheet.vue";

const router = createRouter({
  history: createWebHashHistory("/admin/"),
  routes: [
    {
      name: "RootGen1",
      path: "/",
      component: () => import("../components/RootGen1.vue"),
      meta: {
        title: "20计转本 班级日常事务管理系统"
      }
    },
    {
      name: "HeSuan",
      path: "/admin/hesuan/",
      component: () => import("../components/HeSuan.vue"),
      meta: {
        title: "20计转本-核酸检测"
      }
    },
    {
      name: "WechatClock",
      path: "/admin/wechatclock/",
      component: () => import("../components/WechatClock.vue"),
      meta: {
        title: "20计转本-每日上报"
      }
    },
    {
      name: "SingIn",
      path: "/admin/singin/",
      component: () => import("../components/SingIn.vue"),
      meta: {
        title: "20计转本-签到管理"
      },
      children: [
        {
          name: "SinginTable",
          path: "/admin/singin/",
          component: () => import("../components/Singin_SinginTable.vue"),
          meta: {
            title: '20计转本-签到管理'
          }
        },
        {
          name: "SinginCreateTable",
          path: "/admin/singin/CreateSingin",
          component: () => import("../components/Singin_CreateSingin.vue"),
          meta: {
            title: '20计转本-签到管理-创建签到'
          }
        },
        {
          name: "SinginTableInfo",
          path: "/admin/singin/TableInfo",
          component: () => import("../components/Singin_CreateSingin.vue"),
          meta: {
            title: '20计转本-签到管理-表单编辑'
          }
        },
        {
          name: "SinginTableDetails",
          path: "/admin/singin/TableDetails",
          component: () => import("../components/Singin_TableDetails.vue"),
          meta: {
            title: '20计转本-签到管理-签到详情'
          }
        }
      ]
    },

    {
      name: "CollectFile",
      path: "/admin/collectfile/",
      component: () => import("../components/CollectFile.vue"),
      meta: {
        title: "20计转本-文件收集"
      },
      children: [
        {
          name: "FileTable",
          path: "/admin/collectfile/",
          component: () => import("../components/Collect_FileTable.vue"),
          meta: {
            title: '20计转本-文件收集'
          }
        },
        {
          name: "CreateCollectFile",
          path: "/admin/collectfile/CreateCollect",
          component: () => import("../components/Collect_CreateForm.vue"),
          meta: {
            title: '20计转本-签到管理-新建收集'
          }
        },
        {
          name: "CollectTableInfo",
          path: "/admin/collectfile/TableInfo",
          component: () => import("../components/Collect_CreateForm.vue"),
          meta: {
            title: '20计转本-签到管理-表单编辑'
          }
        },
        {
          name: "CollectTableDetails",
          path: "/admin/collectfile/TableDetails",
          component: () => import("../components/Collect_TableDetails.vue"),
          meta: {
            title: '20计转本-签到管理-收集详情'
          }
        }
      ]

    },
    {
      name: "DocSheet",
      path: "/admin/docsheet/",
      component: () => import("../components/DocSheet.vue"),
      meta: {
        title: "20计转本-电子表格"
      }
    },
    {
      name: "WordSearch",
      path: "/admin/wordsearch/",
      component: () => import("../components/WordSearch.vue"),
      meta: {
        title: "20计转本-姓名检索"
      }
    },
    {
      name: "About",
      path: "/admin/about",
      component: () => import("../components/About.vue"),
      meta: {
        title: "20计转本-项目说明"
      }
    },
  ]
})
router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

export default router;
</script>
