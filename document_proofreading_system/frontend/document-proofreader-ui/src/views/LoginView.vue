<template>
  <div class="login-view">
    <h2>Login</h2>
    <LoginForm @login-submit="handleLogin" />
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import LoginForm from "@/components/LoginForm.vue";
import { mapActions } from "vuex";

export default {
  name: "LoginView",
  components: {
    LoginForm,
  },
  data() {
    return {
      errorMessage: "",
    };
  },
  methods: {
    ...mapActions("auth", ["login"]),
    async handleLogin(credentials) {
      try {
        this.errorMessage = "";
        await this.login(credentials);
        this.$router.push("/dashboard");
      } catch (error) {
        this.errorMessage = error.message || "Failed to login. Please check your credentials.";
        // console.error("Login failed:", error);
      }
    },
  },
};
</script>

<style scoped>
.login-view {
  max-width: 400px;
  margin: auto;
  padding: 20px;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
