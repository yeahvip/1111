import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from 'axios'; // Import axios to set default headers if needed globally

// Attempt to check auth status as early as possible
// This ensures that the store is updated before the app mounts and router guards run
store.dispatch("auth/checkAuth").then(() => {
  // Set Axios default Authorization header after checkAuth has potentially loaded the token
  // This is also handled in checkAuth and login action, but can be a fallback.
  // However, AuthService.js now uses an interceptor, which is a cleaner way.
  // So this explicit setting here might be redundant if interceptor works for all apiClient calls.
  // const token = store.getters["auth/getToken"];
  // if (token) {
  //   axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  // }

  const app = createApp(App);
  app.use(store);
  app.use(router);
  app.mount("#app");
}).catch(error => {
  console.error("Error during auth check on startup:", error);
  // Fallback to mounting the app even if checkAuth fails
  const app = createApp(App);
  app.use(store);
  app.use(router);
  app.mount("#app");
});
