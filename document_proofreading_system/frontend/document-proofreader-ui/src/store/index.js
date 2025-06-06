import { createStore } from "vuex";
import AuthService from "../services/AuthService"; // Will be created in next step
import axios from 'axios'; // For setting auth headers

const authModule = {
  namespaced: true,
  state: {
    token: localStorage.getItem("token") || null,
    user: JSON.parse(localStorage.getItem("user")) || null,
    isAuthenticated: !!localStorage.getItem("token"),
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token;
      state.isAuthenticated = !!token;
      if (token) {
        localStorage.setItem("token", token);
      } else {
        localStorage.removeItem("token");
      }
    },
    SET_USER(state, user) {
      state.user = user;
      if (user) {
        localStorage.setItem("user", JSON.stringify(user));
      } else {
        localStorage.removeItem("user");
      }
    },
    LOGOUT(state) {
      state.token = null;
      state.user = null;
      state.isAuthenticated = false;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await AuthService.login(credentials);
        const token = response.data.access_token;
        // Assuming the backend login response returns the user object or we fetch it separately
        // For now, let's assume token is enough and user details might be fetched later or part of token
        // For simplicity, let's store a dummy user object or decode token if it's a JWT with user info
        // For now, user will be set based on a successful login, but ideally, backend sends user data.
        // Let's assume the backend sends back user info or we make another call.
        // Here, we'll just commit a generic user or extract from token if possible.
        // This part might need adjustment based on actual API response.

        commit("SET_TOKEN", token);
        //axios.defaults.headers.common["Authorization"] = `Bearer ${token}`; // Moved to checkAuth/main.js

        // Placeholder for user data - replace with actual user data from response or a separate API call
        // For now, let's simulate a user object. A real app would get this from the server.
        // const userData = { username: credentials.username }; // Simplified
        // commit("SET_USER", userData);

        // Instead of setting user here, let's assume checkAuth or another mechanism handles user details
        // For now, token implies user is set. The main thing is the token.
        // We might need another action to fetch user details using the token.
        return response; // Return the whole response for flexibility in the component
      } catch (error) {
        if (error.response && error.response.data) {
          throw new Error(error.response.data.message || "Login failed");
        }
        throw new Error(error.message || "Login failed due to network error");
      }
    },
    async register({ commit }, userData) {
      try {
        const response = await AuthService.register(userData);
        // Registration might not automatically log in the user or return a token.
        // Depending on backend behavior, you might commit token/user or just return success.
        return response;
      } catch (error) {
        if (error.response && error.response.data) {
          throw new Error(error.response.data.message || "Registration failed");
        }
        throw new Error(error.message || "Registration failed due to network error");
      }
    },
    logout({ commit }) {
      commit("LOGOUT");
      delete axios.defaults.headers.common["Authorization"];
    },
    checkAuth({ commit, state }) {
      const token = localStorage.getItem("token");
      if (token) {
        commit("SET_TOKEN", token);
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        // Optionally, re-fetch user data if it's not just stored or to verify token validity
        const userString = localStorage.getItem("user");
        if (userString) {
            try {
                commit("SET_USER", JSON.parse(userString));
            } catch(e) {
                commit("SET_USER", null); // Clear if invalid JSON
            }
        } else {
            // If no user in local storage, might need an API call to get user details
            // For now, if token exists, we assume user is somewhat authenticated
            // A robust app would verify token with backend and fetch fresh user data
        }
      } else {
        commit("LOGOUT"); // Ensure state is clean if no token
      }
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    currentUser: (state) => state.user, // Provides access to user data
    getToken: (state) => state.token,
  },
};

export default createStore({
  modules: {
    auth: authModule,
  },
});
