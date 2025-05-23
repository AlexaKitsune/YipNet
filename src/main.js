import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

app.config.globalProperties.$ENDPOINT = 'http://localhost:5001';

app.mount('#app') // usa la misma instancia

