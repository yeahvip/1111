<template>
  <div class="dashboard-view">
    <h2>Dashboard</h2>
    <p>Welcome! You are logged in.</p>
    <p v-if="user">Hello, {{ user.username }}!</p>
    <!-- user might not have username, adjust as per actual user object structure -->
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "DashboardView",
  computed: {
    ...mapGetters("auth", ["currentUser"]), // Using 'currentUser' as defined in task
    user() {
      return this.currentUser;
    }
  },
  created() {
    // You might want to fetch user-specific data here if needed
  }
};
</script>

<style scoped>
.dashboard-view {
  padding: 20px;
}
</style>
