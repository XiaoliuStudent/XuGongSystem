import {createApp} from 'vue'
import '../src/style.css'
import router from './routes/router.vue'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import student from "./student.vue";



const Student = createApp(student)
// Student.use(studentrouter)
// Student.use(Antd)
Student.use(router)
Student.use(ElementPlus)
Student.mount("#app")
