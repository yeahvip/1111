<template>
  <div class="register-view">
    <h2>Register</h2>
    <RegisterForm @register-submit="handleRegister" />
    <p v-if="successMessage" class="success">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import RegisterForm from "@/components/RegisterForm.vue";
import { mapActions } from "vuex";

export default {
  name: "RegisterView",
  components: {
    RegisterForm,
  },
  data() {
    return {
      successMessage: "",
      errorMessage: "",
    };
  },
  methods: {
    ...mapActions("auth", ["register"]),
    async handleRegister(userData) {
      try {
        this.successMessage = "";
        this.errorMessage = "";
        await this.register(userData);
        this.successMessage = "Registration successful! Please login.";
        // Optionally redirect to login or show a message
        // this.$router.push("/login");
      } catch (error) {
        this.errorMessage = error.message || "Registration failed. Please try again.";
        // console.error("Registration failed:", error);
      }
    },
  },
};
</script>

<style scoped>
.register-view {
  max-width: 400px;
  margin: auto;
  padding: 20px;
}
.success {
  color: green;
  margin-top: 10px;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
