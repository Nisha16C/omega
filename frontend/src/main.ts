// main.ts
import type { App } from 'vue';
import { createApp } from 'vue';
import { installRouter } from '@/router';
import { installPinia } from '@/store';
import AppVue from './App.vue';
import AppLoading from './components/common/AppLoading.vue';
import keycloak, { initializeKeycloak } from './plugins/keycloak';

import 'uno.css';


async function setupApp() {
  // Show loading animation during initialization
  const appLoading = createApp(AppLoading);
  appLoading.mount('#appLoading');
 
  // Initialize Keycloak and setup the app only if authenticated
  initializeKeycloak(async () => {
    // If authenticated, create the Vue app
    const app = createApp(AppVue);
 
    // Provide Keycloak globally for access in components
    app.provide('keycloak', keycloak);
 
    
 
    // Install Pinia and Vue Router
    await installPinia(app);
    await installRouter(app);
    await installRouter(app)
 
  /* 注册模块 指令/静态资源 */
  Object.values(
    import.meta.glob<{ install: (app: App) => void }>('./modules/*.ts', {
      eager: true,
    }),
  ).map(i => app.use(i))
 
 
    // Unmount the loading animation and mount the app
    appLoading.unmount();
    app.mount('#app');
 
    // Log confirmation that the app has been mounted
  });
}
 
setupApp();
 
 