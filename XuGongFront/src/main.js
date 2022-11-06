import {createApp} from 'vue'
// import './style.css'
import App from './App.vue'

import router from './routes/router.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css';


import VueQrcode from '@chenfengyuan/vue-qrcode';


import VueMarkdownEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';

VueMarkdownEditor.use(vuepressTheme);



const app = createApp(App)
app.use(router)
app.use(Antd)
app.use(ElementPlus)
app.use(VueMarkdownEditor)
app.component(VueQrcode.name, VueQrcode)
app.mount("#app")
