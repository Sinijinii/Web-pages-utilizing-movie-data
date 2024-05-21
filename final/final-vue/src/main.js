import { createApp } from 'vue'
import { createPinia } from 'pinia'
// 이거 있으니까 실행전에 npm i pinia-plugin-persistedstate 반드시 실행
import PiniaPluginPersistedstate  from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const app = createApp(App)
const pinia = createPinia()

app.use(createPinia())
app.use(router)
pinia.use(PiniaPluginPersistedstate)

app.use(pinia)
app.mount('#app')
