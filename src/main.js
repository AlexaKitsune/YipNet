// main.js
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

const ENDPOINT = 'http://localhost:5001'

async function loadApi() {
    const api = await import(/* webpackIgnore: true */`${ENDPOINT}/endpoints.js`);

    app.config.globalProperties.$ENDPOINT = 'http://localhost:5001';

    Object.entries(api).forEach(([name, fn]) => {
        app.config.globalProperties[name] = fn
    });

    // Desactiva todos los warnings
    app.config.warnHandler = () => {}

    app.mount('#app');
}

loadApi()
