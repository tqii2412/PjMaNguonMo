<template>
    <div class="register-container">
      <h2>Đăng ký</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Username:</label>
          <input v-model="form.username" type="text" required />
        </div>
        <div class="form-group">
          <label>Tên:</label>
          <input v-model="form.name" type="text" required />
        </div>
        <div class="form-group">
          <label>Số điện thoại:</label>
          <input v-model="form.phonenb" type="text" required />
        </div>
        <div class="form-group">
          <label>Mật khẩu:</label>
          <input v-model="form.password" type="password" required />
        </div>
        <div class="form-group">
          <label>Xác nhận mật khẩu:</label>
          <input v-model="form.password_confirm" type="password" required />
        </div>
        <button type="submit">Đăng ký</button>
      </form>
      <p v-if="message">{{ message }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Register',
    data() {
      return {
        form: {
          username: '',
          name: '',
          phonenb: '',
          password: '',
          password_confirm: ''
        },
        message: '',
        error: ''
      };
    },
    methods: {
      async handleRegister() {
        try {
          const response = await axios.post('http://localhost:8000/api/register/', this.form);
          this.message = response.data.message;
          this.error = '';
          this.form = { username: '', name: '', phonenb: '', password: '', password_confirm: '' }; // Reset form
        } catch (err) {
          this.error = err.response?.data?.password || 'Đăng ký thất bại!';
          this.message = '';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .register-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  .form-group {
    margin-bottom: 15px;
  }
  label {
    display: block;
    margin-bottom: 5px;
  }
  input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  button {
    width: 100%;
    padding: 10px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 5px;
  }
  button:hover {
    background-color: #218838;
  }
  .error {
    color: red;
  }
  </style>