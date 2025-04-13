<template>
  <div class="container-fluid py-5 bg-dark text-white min-vh-100">
    <!-- Header trái trên cùng -->
    <div class="d-flex align-items-center mb-4 ps-3">
      <h2 class="m-0">🍓 Fruits</h2>
    </div>

    <!-- Lọc sản phẩm và hiển thị -->
    <div class="row g-4 justify-content-center px-3">
      <div
        v-for="product in filteredProducts"
        :key="product.id"
        class="col-12 col-sm-6 col-md-4 col-lg-3"
      >
        <div
          class="card h-100 shadow-sm border-0 transition-hover overflow-hidden"
          style="background-color: #f8f9fa; color: #212529;"
        >
          <img
            :src="product.detail.image"
            class="product-img-top"
            alt="ảnh sản phẩm"
          />
          <div class="card-body d-flex flex-column justify-content-between p-3">
            <div class="text-center mb-2">
              <h5 class="fw-bold mb-1">{{ product.name }}</h5>
              <p class="text-success fw-semibold mb-1">
                {{ product.price.toLocaleString() }} VNĐ
              </p>
              <p class="text-muted small">
                Xuất xứ: {{ product.detail.origin || "Không rõ" }}
              </p>
            </div>

            <div class="d-flex flex-column justify-content-center align-items-center gap-2 mt-auto">
              <router-link
                :to="`/product/${product.id}`"
                class="btn btn-outline-info btn-sm w-75"
              >
                Xem chi tiết
              </router-link>
              
              <!-- Nút thêm vào giỏ hàng -->
              <add-to-cart-button
                v-if="isLoggedIn"
                :product-id="product.id"
                :price="parseFloat(product.price)"
                :max="product.quantity"
                class="w-75 btn-add-to-cart"
              />
              
              <!-- Khi chưa đăng nhập, hiển thị nút và yêu cầu đăng nhập -->
              <button 
                v-else 
                class="btn btn-outline-warning w-75" 
                @click="handleAddToCart"
              >
                Thêm vào giỏ hàng
              </button>
              <p v-if="showLoginWarning" class="text-danger mt-2 small">
                ⚠️ Bạn cần đăng nhập để thêm vào giỏ hàng.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import AddToCartButton from "../components/AddToCartButton.vue";

export default {
  name: "HomePage",
  components: { AddToCartButton },
  props: {
    searchQuery: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      products: [],
      showLoginWarning: false,
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("user_id");  // Kiểm tra xem người dùng đã đăng nhập hay chưa
    },
    username() {
      return localStorage.getItem("user_id") || "bạn";  // Lấy user_id từ localStorage, nếu không có trả về "bạn"
    },
    filteredProducts() {
      // Lọc sản phẩm theo từ khoá tìm kiếm
      return this.products.filter(product =>
        product.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    async fetchProducts() {
      try {
        const res = await axios.get("http://localhost:8000/api/products/");
        this.products = res.data;
      } catch (error) {
        console.error("Lỗi khi tải sản phẩm:", error);
      }
    },
    handleAddToCart() {
      if (!this.isLoggedIn) {
        // Nếu chưa đăng nhập, hiển thị thông báo yêu cầu đăng nhập
        this.showLoginWarning = true;
        setTimeout(() => {
          this.showLoginWarning = false; // Ẩn thông báo sau 3 giây
        }, 3000);
      } else {
        // Nếu đã đăng nhập, có thể thêm vào giỏ hàng
        console.log("Thêm sản phẩm vào giỏ hàng");
      }
    },
  },
  mounted() {
    this.fetchProducts(); // Lấy danh sách sản phẩm khi trang được tải
  },
};
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Poppins:wght@400;600&display=swap');

body {
  font-family: 'Roboto', sans-serif;
}

.transition-hover {
  transition: transform 0.2s ease-in-out;
}
.transition-hover:hover {
  transform: scale(1.03);
}

.product-img-top {
  aspect-ratio: 1 / 1;
  object-fit: contain;
  width: 100%;
  padding: 10px;
  background-color: white;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
  border-bottom: 1px solid #dee2e6;
}

/* Chỉnh sửa nút "Thêm vào giỏ hàng" với màu nền tối */
.btn-add-to-cart {
  background-color: #343a40; /* Màu nền giống với màu nền trang web */
  color: #fff; /* Chữ màu trắng để dễ đọc */
  border: 1px solid #343a40; /* Đường viền cùng màu với nền */
}

.btn-add-to-cart:hover {
  background-color: #495057; /* Màu khi hover: sáng hơn chút */
  border-color: #495057; /* Đổi màu viền khi hover */
}

.btn-outline-info {
  color: #17a2b8;
  border: 1px solid #17a2b8;
}

.btn-outline-info:hover {
  background-color: #17a2b8;
  color: white;
}

.btn-sm {
  font-size: 0.875rem;
}

h5 {
  font-family: 'Poppins', sans-serif;
}

.card-body {
  padding: 15px;
}
</style>
