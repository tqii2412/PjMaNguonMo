<template>
  <div id="app">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm px-4 py-3">
      <div class="container-fluid d-flex justify-content-between align-items-center">
        <!-- Logo bên trái -->
        <router-link to="/" class="navbar-brand fw-bold">MHMarket</router-link>

        <!-- Thanh tìm kiếm nằm ngay cạnh Logo -->
        <div class="d-flex align-items-center">
          <input
            v-model="searchQuery"
            @input="handleSearch"
            type="text"
            class="form-control"
            placeholder="Tìm kiếm sản phẩm"
            style="width: 300px;"  
          />
        </div>

        <!-- Hamburger Menu cho thiết bị di động -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Thanh điều hướng -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0 d-flex align-items-center gap-3">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Trang chủ</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/about" class="nav-link">About us</router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link to="/login" class="nav-link">Đăng nhập</router-link>
            </li>
            <li class="nav-item dropdown" v-if="isLoggedIn" @click="toggleDropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" aria-expanded="false">
                👋 Xin chào <strong>{{ username }}</strong>
              </a>
              <ul class="dropdown-menu dropdown-menu-end" v-show="dropdownVisible">
                <li>
                  <router-link :to="`/user/${userId}`" class="dropdown-item text-dark fw-normal">Thông tin cá nhân</router-link>
                </li>
                <li>
                  <a class="dropdown-item text-dark fw-normal" href="#" @click.prevent="logout">Đăng xuất</a>
                </li>
              </ul>
            </li>
            <li class="nav-item">
              <router-link to="/cart" class="btn btn-dark">
                Giỏ hàng 🛒
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Nội dung -->
    <router-view :search-query="searchQuery" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "", // Biến lưu trữ giá trị tìm kiếm
      dropdownVisible: false, // Trạng thái dropdown menu
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("user_id");
    },
    username() {
      return localStorage.getItem("username") || "bạn";
    },
    userId() {
      return localStorage.getItem("user_id") || "";
    },
  },
  methods: {
    logout() {
      localStorage.removeItem("user_id");
      localStorage.removeItem("username");
      localStorage.removeItem("token");
      localStorage.removeItem("refresh_token");
      window.location.reload();
    },
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible; // Bật/tắt dropdown
    },
    handleSearch() {
      if (this.searchQuery.trim()) {
        this.$router.push({ path: '/', query: { search: this.searchQuery } });
      }
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

body {
  font-family: 'Roboto', sans-serif;
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

/* Điều chỉnh vị trí thanh tìm kiếm cạnh logo */
.navbar .container-fluid {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar .form-control {
  width: 300px; /* Đặt chiều rộng của thanh tìm kiếm */
  margin-left: 20px; /* Khoảng cách giữa logo và thanh tìm kiếm */
}

@media (max-width: 768px) {
  /* Ẩn thanh tìm kiếm trên các thiết bị di động */
  .search-container {
    display: none;
  }
}
</style>
