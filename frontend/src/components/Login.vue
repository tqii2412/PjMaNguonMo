<template>
    <div class="login-container">
      <h2>Đăng nhập</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Username:</label>
          <input v-model="form.username" type="text" required />
        </div>
        <div class="form-group">
          <label>Mật khẩu:</label>
          <input v-model="form.password" type="password" required />
        </div>
        <button type="submit">Đăng nhập</button>
      </form>
      <p v-if="message">{{ message }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Login',
    data() {
      return {
        form: {
          username: '',
          password: ''
        },
        message: '',
        error: ''
      };
    },
    methods: {
      async handleLogin() {
        try {
          const response = await axios.post('http://localhost:8000/api/login/', this.form);
          this.message = response.data.message;
          this.error = '';
          this.form = { username: '', password: '' }; // Reset form
        } catch (err) {
          this.error = err.response?.data?.error || 'Đăng nhập thất bại!';
          this.message = '';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .login-container {
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
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
  }
  button:hover {
    background-color: #0069d9;
  }
  .error {
    color: red;
  }
  </style>