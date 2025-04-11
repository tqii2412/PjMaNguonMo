<template>
  <div class="login-container d-flex align-items-center justify-content-center min-vh-100 bg-dark text-white">
    <div class="login-box border border-light p-5 rounded" style="min-width: 340px;">
      <h3 class="text-center mb-4">ĐĂNG NHẬP</h3>
      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <input
            v-model="username"
            type="text"
            id="username"
            class="form-control bg-dark text-white border-secondary"
            placeholder="Username"
            required
          />
        </div>
        <div class="mb-3">
          <input
            v-model="password"
            type="password"
            id="password"
            class="form-control bg-dark text-white border-secondary"
            placeholder="Password"
            required
          />
        </div>
        <div class="mb-3 text-center text-secondary" style="font-size: 0.9rem;">
          Chưa có tài khoản?
          <router-link to="/register" class="text-light text-decoration-underline">Đăng ký ngay</router-link>
        </div>
        <button type="submit" class="btn btn-light w-100 fw-bold">ĐĂNG NHẬP</button>
        <p v-if="errorMessage" class="text-danger mt-3 text-center">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "../axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post("login/", {
          username: this.username,
          password: this.password,
        });

        const token = response.data.token;
        if (token) {
          localStorage.setItem("token", token);
        }

        localStorage.setItem("user_id", this.username); // hoặc response.data.user_id nếu có

        alert("Đăng nhập thành công!");
        this.$router.push("/");
      } catch (error) {
        this.errorMessage =
          error.response?.data?.error || "Tên đăng nhập hoặc mật khẩu không đúng";
      }
    },
  },
};
</script>

<style scoped>
.login-box {
  max-width: 400px;
  background-color: #1e1e1e;
}
/* 👇 Highlight placeholder trắng hơn */
::placeholder {
  color: #ccc !important;
  opacity: 1 !important;
}
</style>
