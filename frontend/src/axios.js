// src/axios.js
import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000/api/", // Đặt base URL API của bạn
  headers: {
    "Content-Type": "application/json",
  },
});

export default axiosInstance;
