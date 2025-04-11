<template>
  <div id="app">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg bg-white shadow-sm px-4 py-3">
      <div class="container-fluid">
        <!-- Logo bên trái -->
        <router-link to="/" class="navbar-brand fw-bold">MHMarket</router-link>

        <!-- Group nav items chuyển sang phải -->
        <ul class="navbar-nav ms-auto me-3 mb-2 mb-lg-0 d-flex align-items-center gap-4">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Trang chủ</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/about" class="nav-link">About us</router-link>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link to="/login" class="nav-link">Đăng nhập</router-link>
          </li>
          <li class="nav-item dropdown" v-if="isLoggedIn">
            <a class="nav-link dropdown-toggle d-flex align-items-center gap-1" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
             👋 Xin chào <strong>{{ username }}</strong>
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><a class="dropdown-item text-dark fw-normal" href="#" @click.prevent="logout">Đăng xuất</a></li>
            </ul>
          </li>
        </ul>
        <!-- Nút giỏ hàng nằm cuối -->
        <router-link to="/cart" class="btn btn-dark">
          Giỏ hàng 🛒
        </router-link>
      </div>
    </nav>

    <!-- Nội dung -->
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      loggedIn: !!localStorage.getItem("user_id"),
    };
  },
  computed: {
    isLoggedIn() {
      return this.loggedIn;
    },
    username() {
      return localStorage.getItem("user_id") || "bạn";
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("user_id");
      localStorage.removeItem("token");
      this.loggedIn = false;
      this.$router.push("/");
    },
    checkLoginStatus() {
      this.loggedIn = !!localStorage.getItem("user_id");
    }
  },
  mounted() {
    window.addEventListener("focus", this.checkLoginStatus);
  },
  unmounted() {
    window.removeEventListener("focus", this.checkLoginStatus);
  }
};
</script>

<style>
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  background-color: #f8f9fa;
  margin: 0;
}

.navbar-nav .nav-link {
  font-weight: 500;
  color: #2c3e50;
}

.navbar-nav .nav-link.router-link-exact-active {
  color: #42b983;
}

.btn-link {
  text-decoration: none;
}
</style>
