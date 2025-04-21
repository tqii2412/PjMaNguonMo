<template>
    <div class="user-profile-container">
      <!-- User Info Section -->
      <div class="user-info-container">
        <div v-if="user" class="user-info">
          <h1>Chào, {{ user.name }}</h1>
          <p><strong>Username:</strong> {{ user.username }}</p>
          <p><strong>Tên:</strong> {{ user.name }}</p>
          <p><strong>Số điện thoại:</strong> {{ user.phonenb }}</p>
        </div>
        <div v-else>
          <p>Đang tải thông tin...</p>
        </div>
  
        <!-- User Actions -->
        <div class="user-actions">
          <router-link to="/edit-profile" class="btn btn-primary btn-lg">Chỉnh sửa thông tin</router-link>
          <button @click="logout" class="btn btn-danger btn-lg">Đăng xuất</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import api from '../axios'; 
  
  export default {
    props: ['id'],
    data() {
      return {
        user: null,
      };
    },
    mounted() {
      this.fetchUserInfo();
    },
    methods: {
      async fetchUserInfo() {
        try {
          const userId = this.id || localStorage.getItem("user_id");
          if (!userId) {
            console.error("Không tìm thấy userId.");
            return;
          }
  
          const response = await api.get(`users/${userId}/`);
          this.user = response.data;
        } catch (error) {
          console.error("Lỗi khi lấy thông tin người dùng", error);
        }
      },
      logout() {
        // Logic for logging out
        this.$router.push('/login');
      }
    },
  };
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Roboto:wght@500;700&display=swap');
  
  .user-profile-container {
    background-color: #fff;
    padding: 50px 15%;
    font-family: 'Roboto', sans-serif;
  }
  
  .user-info-container {
    background-color: #f8f9fa;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .user-info h1 {
    font-size: 2.5rem;
    font-family: 'Poppins', sans-serif;
    color: #4CAF50;
    margin-bottom: 20px;
  }
  
  .user-info p {
    font-size: 1.125rem;
    margin: 10px 0;
  }
  
  .user-actions {
    text-align: center;
    margin-top: 30px;
  }
  
  .user-actions .btn {
    font-size: 1.125rem;
    padding: 12px 40px;
    border-radius: 30px;
    font-weight: 600;
    transition: all 0.3s ease;
    margin-top: 20px;
  }
  
  .user-actions .btn-primary {
    background-color: #4CAF50;
    color: #fff;
    border: none;
  }
  
  .user-actions .btn-danger {
    background-color: #e74c3c;
    color: #fff;
    border: none;
  }
  
  .user-actions .btn:hover {
    opacity: 0.8;
  }
  </style>
  