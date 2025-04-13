const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: 'http://localhost:8000',  // Cấu hình proxy để giao tiếp với backend Django
  },
  configureWebpack: {
    resolve: {
      alias: {
        vue$: 'vue/dist/vue.esm-bundler.js',  // Đảm bảo sử dụng Vue với esm-bundler
      },
    },
  },
  chainWebpack: (config) => {
    // Thiết lập feature flags cho Vue khi sử dụng esm-bundler build
    config.plugin('define').tap((args) => {
      args[0]['__VUE_PROD_HYDRATION_MISMATCH_DETAILS__'] = JSON.stringify('true');
      return args;
    });
  },
});
