import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  define: {
    // Đảm bảo rằng các flag cần thiết được định nghĩa
    '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': JSON.stringify('true'),
  },
})
