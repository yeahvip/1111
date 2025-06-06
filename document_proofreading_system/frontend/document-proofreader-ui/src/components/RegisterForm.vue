<template>
  <form @submit.prevent="handleSubmit">
    <div>
      <label for="username">Username:</label>
      <input type="text" id="username" v.model="username" required />
    </div>
    <div>
      <label for="password">Password:</label>
      <input type="password" id="password" v.model="password" required />
    </div>
    <div>
      <label for="confirmPassword">Confirm Password:</label>
      <input type="password" id="confirmPassword" v.model="confirmPassword" required />
    </div>
    <button type="submit">Register</button>
    <p v-if="passwordMismatch" class="error">Passwords do not match.</p>
  </form>
</template>

<script>
export default {
  name: "RegisterForm",
  data() {
    return {
      username: "",
      password: "",
      confirmPassword: "",
      passwordMismatch: false,
    };
  },
  methods: {
    handleSubmit() {
      this.passwordMismatch = false;
      if (this.password !== this.confirmPassword) {
        this.passwordMismatch = true;
        return;
      }
      this.$emit("register-submit", {
        username: this.username,
        password: this.password,
      });
    },
  },
};
</script>

<style scoped>
form div {
  margin-bottom: 10px;
}
.error {
  color: red;
}
</style>
