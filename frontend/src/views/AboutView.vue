<template>
  <div class="about-container">
    <!-- Hero Section -->
    <div class="hero-section d-flex justify-content-center align-items-center">
      <div class="overlay"></div> <!-- Lớp phủ mờ trên hình nền -->
      <div class="hero-text text-center text-white">
        <h1 class="display-4 fw-bold">Shop Now</h1>
        <p class="lead fw-semibold">Tươi – Sạch – Giao tận tay. Trái cây chất lượng cho mọi nhà.</p>
        <router-link to="/" class="btn btn-light btn-lg mt-3 shop-btn">
          Shop
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AboutView",
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Roboto:wght@500;700&display=swap');

/* Hero Section */
.hero-section {
  position: relative;
  background-image: url('D:\source django\pj2\frontend\public\dualoai2.jpg'); /* Đảm bảo sử dụng đúng tên file ảnh */
  background-size: cover;
  background-position: center;
  height: 100vh;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4); /* Lớp phủ màu đen với độ mờ 40% */
  z-index: 1; /* Đảm bảo lớp phủ chỉ nằm trên ảnh */
}

.hero-text {
  position: relative;
  z-index: 2; /* Đảm bảo văn bản và nút nằm trên lớp phủ */
}

.hero-text h1 {
  font-size: 4rem;
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
}

.hero-text p {
  font-size: 1.25rem;
  font-family: 'Roboto', sans-serif;
  font-weight: 500;
}

.hero-text .shop-btn {
  font-size: 1.125rem;
  padding: 10px 30px;
  border-radius: 30px;
  font-weight: 600;
  transition: all 0.3s ease;
  background-color: #f8f9fa;
  color: #212529;
  border: 1px solid #ddd;
}

.hero-text .shop-btn:hover {
  background-color: #000;
  color: #fff;
  border-color: #000;
}

/* Nội dung giới thiệu */
.about-content {
  text-align: center;
  margin-top: 50px;
}

.about-content h1 {
  font-size: 2.5rem;
  font-family: 'Poppins', sans-serif;
}

.about-content p {
  font-size: 1.125rem;
  font-family: 'Roboto', sans-serif;
}
</style>
