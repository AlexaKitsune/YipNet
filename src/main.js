import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

app.config.globalProperties.$ENDPOINT = 'http://192.168.100.11:5001';

app.mount('#app') // usa la misma instancia

