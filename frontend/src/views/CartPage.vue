<template>
  <div class="container-fluid py-5 bg-dark text-white min-vh-100">
    <h2 class="mb-4 ps-3">🛒 Giỏ Hàng</h2>

    <!-- Loading State -->
    <div v-if="loading" class="text-center text-muted">
      <p>Đang tải giỏ hàng...</p>
    </div>

    <!-- Giỏ hàng có sản phẩm -->
    <div
      v-if="cart && cart.items && Array.isArray(cart.items) && cart.items.length > 0"
      class="px-3"
    >
      <div
        v-for="item in cart.items"
        :key="item.product_detail.id"
        class="card mb-4 shadow-sm border-0 overflow-hidden"
        style="background-color: #f8f9fa; color: #212529;"
      >
        <div class="row g-0 align-items-center">
          <!-- Ảnh sản phẩm -->
          <div class="col-md-3 p-3">
            <img
              :src="item.product_detail.image"
              alt="Ảnh sản phẩm"
              class="img-fluid rounded product-img"
              style="background: white; aspect-ratio: 1/1; object-fit: contain;"
            />
          </div>

          <!-- Nội dung sản phẩm -->
          <div class="col-md-9">
            <div class="card-body">
              <h5 class="fw-bold mb-2">{{ item.product_detail.name }}</h5>
              <p class="mb-1">
                Giá:
                <span class="text-success fw-semibold">
                  {{ item.product_detail.price.toLocaleString() }} VNĐ
                </span>
              </p>
              <p class="mb-1">Số lượng: {{ item.quantity }}</p>
              <p class="mb-1 fw-medium">
                Tổng giá:
                <span class="text-primary fw-semibold">
                  {{ (item.product_detail.price * item.quantity).toLocaleString() }} VNĐ
                </span>
              </p>
              <!-- Nút xóa sản phẩm -->
              <button
                class="btn btn-danger mt-2"
                @click="removeItem(item.product_detail.id)"
              >
                Xóa
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Tổng giá trị -->
      <div class="text-end pe-3 mt-4">
        <h4 class="fw-bold text-white">
          Tổng giá trị giỏ hàng:
          <span class="text-success">
            {{ cart.items.reduce((sum, item) => sum + item.product_detail.price * item.quantity, 0).toLocaleString() }} VNĐ
          </span>
        </h4>

        <button class="btn btn-success mt-3 px-4 py-2" @click="handleCheckout">
          Thanh toán
        </button>
      </div>
    </div>

    <!-- Giỏ hàng trống -->
    <div v-else class="text-center text-muted pt-5">
      <p v-if="emptyCart">🛒 Giỏ hàng của bạn hiện tại chưa có sản phẩm nào.</p>
      <p v-else>Đang tải giỏ hàng...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      cart: null,
      loading: true,
      emptyCart: false,
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("user_id");
    },
  },
  methods: {
    // Lấy dữ liệu giỏ hàng
    async fetchCart() {
      if (this.isLoggedIn) {
        try {
          const userId = localStorage.getItem("user_id");
          const token = localStorage.getItem("token");
          const config = {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          };

          const res = await axios.get(
            `http://localhost:8000/api/cartorders/?user=${userId}&status=pending`,
            config
          );
          console.log("Dữ liệu giỏ hàng: ", res.data); // Kiểm tra dữ liệu trả về

          if (res.data && res.data.length > 0) {
            this.cart = res.data[0];
            this.emptyCart = false;
          } else {
            this.cart = null;
            this.emptyCart = true;
          }
        } catch (error) {
          console.error("Lỗi khi lấy giỏ hàng:", error);
          alert("Không thể tải giỏ hàng. Vui lòng thử lại.");
        } finally {
          this.loading = false;
        }
      } else {
        this.$router.push("/login");
      }
    },

    // Xóa sản phẩm khỏi giỏ hàng
    async removeItem(productId) {
      const token = localStorage.getItem("token");
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      try {
        // Gửi yêu cầu xóa sản phẩm
        const res = await axios.delete(
          `http://localhost:8000/api/cart/item/${productId}/remove/`,
          config
        );
        console.log(res.data); // Kiểm tra kết quả trả về

        // Cập nhật lại giỏ hàng sau khi xóa sản phẩm
        this.cart.items = this.cart.items.filter(
          (item) => item.product_detail.id !== productId
        );
        
        // Cập nhật tổng giá trị giỏ hàng
        this.cart.itemsTotal = this.cart.items.reduce(
          (sum, item) => sum + item.product_detail.price * item.quantity,
          0
        );
        alert("Sản phẩm đã được xóa khỏi giỏ hàng.");
      } catch (error) {
        console.error("Lỗi khi xóa sản phẩm:", error);
        alert("Có lỗi xảy ra khi xóa sản phẩm.");
      }
    },

    // Xử lý thanh toán
    handleCheckout() {
      if (this.cart && this.cart.items && this.cart.items.length > 0) {
        alert("Thanh toán giỏ hàng.");
        this.$router.push("/payment");
      } else {
        alert("Giỏ hàng của bạn không có sản phẩm.");
      }
    },
  },
  mounted() {
    if (!this.isLoggedIn) {
      this.$router.push("/login");
    } else {
      this.fetchCart(); // Lấy danh sách sản phẩm khi trang được tải
    }
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Poppins:wght@400;600&display=swap");

h2,
h5,
p {
  font-family: "Poppins", sans-serif;
}

.card-body {
  padding: 20px;
}

.product-img {
  border-radius: 1rem;
  padding: 5px;
  border: 1px solid #dee2e6;
  width: 100%;
}

.btn {
  font-family: "Roboto", sans-serif;
}
</style>
