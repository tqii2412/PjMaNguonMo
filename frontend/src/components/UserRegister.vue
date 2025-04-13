<template>
  <div class="register-container d-flex align-items-center justify-content-center min-vh-100 bg-dark text-white">
    <div class="register-box border border-light p-5 rounded" style="min-width: 340px;">
      <h3 class="text-center mb-4">ĐĂNG KÝ</h3>
      <form @submit.prevent="registerUser">
        <div class="mb-3">
          <input
            v-model="username"
            type="text"
            class="form-control bg-dark text-white border-secondary"
            placeholder="Tên Đăng Nhập"
            required
          />
        </div>
        <div class="mb-3">
          <input
            v-model="name"
            type="text"
            class="form-control bg-dark text-white border-secondary"
            placeholder="Họ và Tên"
            required
          />
        </div>
        <div class="mb-3">
          <input
            v-model="phonenb"
            type="text"
            class="form-control bg-dark text-white border-secondary"
            placeholder="Số Điện Thoại"
            required
          />
        </div>
        <div class="mb-3">
          <input
            v-model="password"
            type="password"
            class="form-control bg-dark text-white border-secondary"
            placeholder="Mật khẩu"
            required
          />
        </div>
        <div class="mb-3">
          <input
            v-model="password_confirm"
            type="password"
            class="form-control bg-dark text-white border-secondary"
            placeholder="Xác nhận mật khẩu"
            required
          />
        </div>
        <div class="mb-3 text-center text-secondary" style="font-size: 0.9rem;">
          Đã có tài khoản?
          <router-link to="/login" class="text-light text-decoration-underline">Đăng nhập ngay</router-link>
        </div>
        <button type="submit" class="btn btn-light w-100 fw-bold">ĐĂNG KÝ</button>
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
      name: "",
      phonenb: "",
      password: "",
      password_confirm: "",
      errorMessage: "",
    };
  },
  methods: {
    async registerUser() {
      try {
        await axios.post("register/", {
          username: this.username,
          name: this.name,
          phonenb: this.phonenb,
          password: this.password,
          password_confirm: this.password_confirm,
        });

        alert("Đăng ký thành công!");
        this.$router.push("/login");
      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage =
            error.response.data.password ||
            error.response.data.non_field_errors ||
            "Có lỗi xảy ra";
        } else {
          this.errorMessage = "Lỗi kết nối với máy chủ. Vui lòng thử lại.";
        }
      }
    },
  },
};
</script>

<style scoped>
.register-box {
  max-width: 420px;
  background-color: #1e1e1e;
}

::placeholder {
  color: #ccc !important;
  opacity: 1 !important;
}
</style>
