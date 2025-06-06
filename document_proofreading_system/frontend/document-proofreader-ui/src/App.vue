<template>
  <div id="app-container">
    <nav>
      <router-link to="/">Home (Redirects)</router-link> |
      <template v-if="isAuthenticated">
        <router-link to="/dashboard">Dashboard</router-link> |
        <a href="#" @click.prevent="handleLogout">Logout</a>
      </template>
      <template v-else>
        <router-link to="/login">Login</router-link> |
        <router-link to="/register">Register</router-link>
      </template>
    </nav>
    <router-view />
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "App",
  computed: {
    ...mapGetters("auth", ["isAuthenticated"]),
  },
  methods: {
    ...mapActions("auth", ["logout"]),
    handleLogout() {
      this.logout();
      this.$router.push("/login"); // Redirect to login after logout
    },
  },
};
</script>

<style>
#app-container { /* Changed from #app to avoid conflict if Vue injects #app itself */
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}

nav {
  padding: 20px;
  background-color: #f0f0f0;
  border-bottom: 1px solid #ddd;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  margin: 0 10px;
  text-decoration: none;
}

nav a.router-link-exact-active {
  color: #42b983;
}

nav a:hover {
  text-decoration: underline;
}
</style>
