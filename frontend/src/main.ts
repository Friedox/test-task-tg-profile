import { createApp } from 'vue'
import App from './App.vue'
import pinia from './store/index.ts'
import router from './router.ts'
import './styles.css'

createApp(App).use(pinia).use(router).mount('#app')