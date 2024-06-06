import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.config.globalProperties.$ENDPOINT = 'http://localhost:5000' // Replace with backend server.

app.mount('#app')
