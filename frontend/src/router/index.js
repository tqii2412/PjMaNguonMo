import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import UserLogin from "../components/UserLogin.vue";
import UserRegister from "../components/UserRegister.vue";
import CartPage from "../views/CartPage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage,
  },
  {
    path: "/register", // Đường dẫn cho trang đăng ký
    name: "register",
    component: UserRegister,
  },
  {
    path: "/login", // Đường dẫn cho trang đăng nhập
    name: "login",
    component: UserLogin,
  },
  {
    path: "/about",
    name: "about",
    component: () => import("@/views/AboutView.vue")
  },
  {
    path: "/product/:id",
    name: "product-detail",
    component: () => import("../views/ProductDetail.vue")
  },
  {
    path: "/cart",
    name: "cart",
    component: CartPage,  // Đảm bảo thêm CartPage vào router
    beforeEnter: (to, from, next) => {
      const userId = localStorage.getItem("user_id");
      if (!userId) {
        // Bạn có thể thêm thông báo hoặc xử lý gì đó khi chuyển hướng
        alert("Bạn cần đăng nhập để tiếp tục.");
        next({ name: "login" });  // Nếu chưa đăng nhập, chuyển hướng đến login
      } else {
        next();  // Nếu đã đăng nhập, tiếp tục điều hướng
      }
    }
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
