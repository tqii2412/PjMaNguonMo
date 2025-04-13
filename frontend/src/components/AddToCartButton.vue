<template>
  <button @click="handleAddToCart" class="btn">
    Thêm vào giỏ hàng
  </button>
</template>

<script>
import axios from "../axios"; // Đảm bảo axios đã được cấu hình sẵn

export default {
  props: {
    productId: Number,
    price: {
      type: Number, // Đảm bảo rằng giá trị này là kiểu Number
      required: true
    },
    max: {
      type: Number,
      required: true
    },
  },
  data() {
    return {
      quantity: 1, // Số lượng mặc định là 1
    };
  },
  methods: {
    async handleAddToCart() {
      const userId = localStorage.getItem("user_id"); // Lấy user_id từ localStorage
      if (!userId) {
        // Nếu người dùng chưa đăng nhập, hiển thị cảnh báo
        this.$router.push("/login"); // Chuyển người dùng đến trang đăng nhập
        return;
      }

      // Kiểm tra số lượng người dùng nhập
      if (this.quantity <= 0 || this.quantity > this.max) {
        alert(`Số lượng không hợp lệ. Vui lòng chọn số lượng từ 1 đến ${this.max}.`);
        return;
      }

      try {
        let token = localStorage.getItem("token");  // Lấy token từ localStorage
        if (!token) {
          alert("⚠️ Vui lòng đăng nhập để thực hiện thao tác này.");
          this.$router.push("/login");  // Chuyển hướng người dùng đến trang đăng nhập
          return;
        }

        let config = {
          headers: {
            Authorization: `Bearer ${token}`,  // Gửi token dưới dạng Bearer token
          }
        };

        // Lấy giỏ hàng của người dùng
        let cartOrderResponse = await axios.get(`cartorders/?user=${userId}&status=pending`, config);  // Sử dụng userId thay vì username
        let cartOrder = cartOrderResponse.data[0]; // Giả sử chỉ có một giỏ hàng pending cho người dùng

        if (!cartOrder) {
          // Nếu không có giỏ hàng, tạo một giỏ hàng mới
          cartOrder = await axios.post("cartorders/", {
            user: userId,  // Gửi userId thay vì username
            total_price: this.price * this.quantity, // Tính tổng giá trị giỏ hàng
          }, config);
        }

        // Thêm sản phẩm vào giỏ hàng
        await axios.post("cartorderitems/", {
          order: cartOrder.id, // Giỏ hàng đang pending
          product: this.productId, // ID sản phẩm
          price: parseFloat(this.price), // Giá sản phẩm (chuyển giá trị từ string sang number)
          quantity: this.quantity, // Số lượng sản phẩm
        }, config);

        alert("✅ Đã thêm vào giỏ hàng!");

      } catch (err) {
        console.error("Lỗi khi thêm vào giỏ hàng:", err);
        if (err.response && err.response.status === 401) {
          const refreshToken = localStorage.getItem("refresh_token");  // Lấy refresh token từ localStorage

          if (!refreshToken) {
            alert("Token hết hạn và không có refresh token. Vui lòng đăng nhập lại.");
            this.$router.push("/login");
            return;
          }

          try {
            // Gửi yêu cầu làm mới token
            const refreshResponse = await axios.post("http://localhost:8000/api/token/refresh/", { refresh: refreshToken });

            const newAccessToken = refreshResponse.data.access;
            localStorage.setItem("token", newAccessToken);  // Cập nhật lại token

            // Tiến hành thêm sản phẩm vào giỏ hàng sau khi làm mới token
            await this.handleAddToCart();
          } catch (refreshError) {
            alert("Không thể làm mới token. Vui lòng đăng nhập lại.");
            this.$router.push("/login");
          }
        } else {
          alert("❌ Đã có lỗi xảy ra khi thêm sản phẩm vào giỏ hàng.");
        }
      }
    }
  }
};
</script>

<style scoped>
.btn {
  margin-top: 10px;
  padding: 6px 12px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #1976d2;
}
</style>
