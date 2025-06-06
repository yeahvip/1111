<template>
  <form @submit.prevent="handleSubmit">
    <div>
      <label for="username">Username/Email:</label>
      <input type="text" id="username" v.model="username" required />
    </div>
    <div>
      <label for="password">Password:</label>
      <input type="password" id="password" v.model="password" required />
    </div>
    <button type="submit">Login</button>
  </form>
</template>

<script>
export default {
  name: "LoginForm",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    handleSubmit() {
      this.$emit("login-submit", {
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
</style>
