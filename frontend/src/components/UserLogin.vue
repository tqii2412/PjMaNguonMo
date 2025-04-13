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

        const accessToken = response.data.access;
        const refreshToken = response.data.refresh;
        const userId = response.data.user_id;

        if (accessToken && userId) {
          localStorage.setItem("token", accessToken);
          localStorage.setItem("refresh_token", refreshToken);
          localStorage.setItem("user_id", userId);

          const userInfo = await axios.get(`http://localhost:8000/api/users/${userId}/`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });

          localStorage.setItem("username", userInfo.data.username);
        }

        alert("Đăng nhập thành công!");

        // 👉 Điều hướng trước, sau đó reload để cập nhật navbar
        this.$router.push("/");
        setTimeout(() => {
          window.location.reload();
        }, 100);
      } catch (error) {
        this.errorMessage =
          error.response?.data?.error || "Tên đăng nhập hoặc mật khẩu không đúng";
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  background-color: #1e1e1e;
}

.login-box {
  max-width: 400px;
  background-color: #1e1e1e;
}

::placeholder {
  color: #ccc !important;
  opacity: 1 !important;
}

.form-control {
  background-color: #2c2f35;
  color: white;
  border: 1px solid #444;
}

.form-control:focus {
  background-color: #444;
  border-color: #17a2b8;
}

.btn-light {
  background-color: #17a2b8;
  color: white;
  border: none;
}

.btn-light:hover {
  background-color: #138496;
}

.text-decoration-underline {
  text-decoration: underline;
}

.text-danger {
  font-size: 0.875rem;
}
</style>
