<script>
import {createRouter, createWebHashHistory} from 'vue-router';
import studentsingin from "../components/studentsingin.vue";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      name: "RootGen1",
      path: "/",
      component: () => import("../components/RootGen1.vue"),
      meta: {
        title: "20计转本-学生端系统"
      }
    },
    {
      name: "CollectFile",
      path: "/student/collectfile",
      component: () => import("../components/studentcollectfile.vue"),
      meta: {
        title: "20计转本-学生文件上传"
      }
    },
    {
      name: "StudentSingIn",
      path: "/student/singin",
      component: () => import("../components/studentsingin.vue"),
      meta: {
        title: "20计转本-学生签到"
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
