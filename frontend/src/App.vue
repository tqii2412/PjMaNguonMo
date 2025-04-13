<template>
  <div id="app">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg bg-white shadow-sm px-4 py-3">
      <div class="container-fluid">
        <!-- Logo bên trái -->
        <router-link to="/" class="navbar-brand fw-bold">MHMarket</router-link>

        <!-- Thanh tìm kiếm -->
        <form class="d-flex ms-3" @submit.prevent="handleSearch">
          <input
            v-model="searchQuery"
            class="form-control me-2 search-input"
            type="search"
            placeholder="Tìm sản phẩm..."
            aria-label="Search"
          />
          <button class="btn search-btn" type="submit">Tìm</button>
        </form>

        <!-- Các items khác trong navbar -->
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
              <li>
                <a class="dropdown-item text-dark fw-normal" href="#" @click.prevent="logout">Đăng xuất</a>
              </li>
            </ul>
          </li>
        </ul>

        <!-- Nút giỏ hàng -->
        <router-link to="/cart" class="btn btn-dark">
          Giỏ hàng 🛒
        </router-link>
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
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("user_id");
    },
    username() {
      return localStorage.getItem("username") || "bạn";
    },
  },
  methods: {
    logout() {
      // Xoá dữ liệu phiên
      localStorage.removeItem("user_id");
      localStorage.removeItem("username");
      localStorage.removeItem("token");
      localStorage.removeItem("refresh_token");

      // Reload lại trang để cập nhật toàn bộ UI
      window.location.reload();
    },
    handleSearch() {
      // Chuyển hướng tới HomePage và truyền query tìm kiếm vào URL
      if (this.searchQuery.trim()) {
        this.$router.push({ path: '/', query: { search: this.searchQuery } });
      }
    },
  },
};
</script>

<style>
/* Sử dụng font chữ đẹp từ Google Fonts */
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

.btn-link {
  text-decoration: none;
}

/* Thay đổi cho thanh tìm kiếm */
.search-input {
  width: 500px;  /* Tăng chiều dài của thanh tìm kiếm */
  border-radius: 30px; /* Bo góc */
  padding-left: 20px; /* Khoảng cách trái cho chữ */
  border: 1px solid #ced4da; /* Đảm bảo border rõ ràng */
  transition: all 0.3s ease; /* Hiệu ứng chuyển tiếp khi hover */
}

.search-input:focus {
  border-color: #42b983; /* Màu viền khi focus */
  box-shadow: 0 0 5px rgba(66, 185, 131, 0.5); /* Thêm hiệu ứng shadow */
}

/* Cải tiến nút tìm kiếm */
.search-btn {
  border-radius: 30px; /* Bo góc cho nút tìm kiếm */
  background-color: black; /* Màu nền đen */
  color: white;
  transition: background-color 0.3s ease-in-out;
  padding: 5px 15px; /* Cải thiện padding cho nút */
  margin-left: 10px; /* Khoảng cách giữa nút và thanh tìm kiếm */
  font-weight: 500; /* Font chữ đẹp */
}

.search-btn:hover {
  background-color: #333; /* Màu đen tối hơn khi hover */
}

/* Tăng độ tương phản cho các mục trong navbar */
.navbar-nav .nav-link {
  font-weight: 500;
  color: #2c3e50;
}

.navbar-nav .nav-link.router-link-exact-active {
  color: #42b983;
}
</style>
