<template>
    <button @click="handleAddToCart" class="btn">
      Thêm vào giỏ hàng
    </button>
  </template>
  
  <script>
  import axios from "../axios";
  
  export default {
    props: {
      productId: Number,
      price: Number,
      max: Number
    },
    methods: {
      async handleAddToCart() {
        const userId = localStorage.getItem("user_id");
        if (!userId) {
          alert("⚠️ Vui lòng đăng nhập để thêm vào giỏ hàng.");
          this.$router.push("/login");
          return;
        }
  
        try {
          await axios.post("cartorders/", {
            user: userId,
            total_price: this.price, // Đơn giản hóa demo
          });
  
          alert("✅ Đã thêm vào giỏ hàng!");
        } catch (err) {
          console.error("Lỗi thêm vào giỏ hàng:", err);
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
  }
  </style>
  