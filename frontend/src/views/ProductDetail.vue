<template>
  <div class="container-fluid py-5 bg-dark text-white min-vh-100 d-flex justify-content-center align-items-start">
    <div
      v-if="product && product.detail && !isNaN(parseFloat(product.price))"
      class="product-detail-wrapper p-3 rounded shadow"
      style="max-width: 360px; width: 100%; background-color: #f8f9fa; color: #212529;"
    >
      <img
        :src="product.detail.image"
        alt="Ảnh sản phẩm"
        class="product-img-top mb-3"
      />
      <div class="text-center">
        <h6 class="fw-bold mb-2">{{ product.name }}</h6>
        <p class="text-success fw-semibold mb-1 fs-6">
          {{ parseFloat(product.price).toLocaleString() }} VNĐ
        </p>
        <p class="text-muted small mb-2">
          <strong>Xuất xứ:</strong> {{ product.detail.origin || "Không rõ" }}
        </p>
        <p class="small mb-1">
          <strong>Mô tả:</strong> {{ product.detail.description || "Không có mô tả." }}
        </p>
        <p class="small">
          <strong>Dinh dưỡng:</strong> {{ product.detail.nutrition_info || "Không có thông tin." }}
        </p>

        <div class="mt-3">
          <add-to-cart-button
            v-if="isLoggedIn"
            :product-id="product.id"
            :price="parseFloat(product.price)"
            :max="product.quantity"
            class="w-75 btn-add-to-cart"
          />
          <p v-else class="text-danger mt-2 small">
            ⚠️ Bạn cần đăng nhập để thêm vào giỏ hàng.
          </p>
        </div>
      </div>
    </div>

    <!-- Loading hoặc lỗi -->
    <div v-else class="text-center text-light mt-5">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Đang tải...</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import AddToCartButton from "../components/AddToCartButton.vue";

export default {
  name: "ProductDetail",
  components: { AddToCartButton },
  data() {
    return {
      product: null,
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("user_id");
    },
  },
  async created() {
    const id = this.$route.params.id;
    try {
      const res = await axios.get(`http://localhost:8000/api/products/${id}/`);
      this.product = res.data;
    } catch (error) {
      console.error("Lỗi tải chi tiết sản phẩm:", error);
    }
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Poppins:wght@400;600&display=swap');

body {
  font-family: 'Roboto', sans-serif;
}

.product-detail-wrapper {
  background-color: #f8f9fa;
  color: #212529;
}

.product-img-top {
  aspect-ratio: 1 / 1;
  object-fit: contain;
  width: 100%;
  background-color: white;
  border-radius: 1rem;
  border-bottom: 1px solid #dee2e6;
}

h6 {
  font-family: 'Poppins', sans-serif;
}

/* Cải tiến cho nút "Thêm vào giỏ hàng" */
.btn-add-to-cart {
  background-color: #343a40; /* Màu nền giống với màu nền trang web */
  color: #fff; /* Chữ màu trắng để dễ đọc */
  border: 1px solid #343a40; /* Đường viền cùng màu với nền */
}

.btn-add-to-cart:hover {
  background-color: #495057; /* Màu khi hover: sáng hơn chút */
  border-color: #495057; /* Đổi màu viền khi hover */
}

/* Cải thiện khoảng cách và bố cục */
.product-detail-wrapper {
  padding: 15px;
  border-radius: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.product-detail-wrapper .text-center {
  margin-bottom: 15px;
}

.product-detail-wrapper .text-muted {
  font-size: 0.875rem;
}
</style>
