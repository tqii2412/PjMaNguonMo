<template>
  <div class="container-fluid py-5 bg-dark text-white min-vh-100">
    <!-- Header trái trên cùng -->
    <div class="d-flex align-items-center mb-4 ps-3">
      <h2 class="m-0">🍓 Fruits</h2>
    </div>

    <div class="row g-4 justify-content-center px-3">
      <div
        v-for="product in products"
        :key="product.id"
        class="col-12 col-sm-6 col-md-4 col-lg-3"
      >
        <div
          class="card h-100 shadow-sm border-0 transition-hover overflow-hidden"
          style="background-color: #f8f9fa; color: #212529;"
        >
          <img
            :src="product.detail.image"
            class="product-img-top"
            alt="ảnh sản phẩm"
          />
          <div class="card-body d-flex flex-column justify-content-between p-3">
            <div class="text-center mb-2">
              <h5 class="fw-bold mb-1">{{ product.name }}</h5>
              <p class="text-success fw-semibold mb-1">
                {{ product.price.toLocaleString() }}₫
              </p>
              <p class="text-muted small">
                Xuất xứ: {{ product.detail.origin || "Không rõ" }}
              </p>
            </div>

            <div class="d-flex flex-wrap justify-content-center gap-2 mt-auto">
              <router-link
                :to="`/product/${product.id}`"
                class="btn btn-outline-primary btn-sm"
              >
                Xem chi tiết
              </router-link>
              <add-to-cart-button
                v-if="isLoggedIn"
                :product-id="product.id"
                :price="product.price"
                :max="product.quantity"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import AddToCartButton from "../components/AddToCartButton.vue";

export default {
  name: "HomePage",
  components: { AddToCartButton },
  data() {
    return {
      products: [],
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("user_id");
    },
  },
  methods: {
    async fetchProducts() {
      try {
        const res = await axios.get("http://localhost:8000/api/products/");
        this.products = res.data;
      } catch (error) {
        console.error("Lỗi khi tải sản phẩm:", error);
      }
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>

<style scoped>
.transition-hover {
  transition: transform 0.2s ease-in-out;
}
.transition-hover:hover {
  transform: scale(1.03);
}

.product-img-top {
  aspect-ratio: 1 / 1;
  object-fit: contain;
  width: 100%;
  padding: 10px;
  background-color: white;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
  border-bottom: 1px solid #dee2e6;
}
</style>
