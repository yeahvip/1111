import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue"; // Keep for root redirect logic for now
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import DashboardView from "../views/DashboardView.vue";
import store from "../store"; // Import the Vuex store

const routes = [
  {
    path: "/",
    name: "home",
    // component: HomeView, // Or redirect immediately
    redirect: () => {
      // Redirect based on auth status
      return store.getters["auth/isAuthenticated"] ? "/dashboard" : "/login";
    },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: { guest: true }, // For redirecting logged-in users from login page
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
    meta: { guest: true }, // For redirecting logged-in users from register page
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashboardView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters["auth/isAuthenticated"];

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: "login" });
    } else {
      next();
    }
  } else if (to.matched.some((record) => record.meta.guest)) {
    if (isAuthenticated) {
      next({ name: "dashboard" });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
