import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import UserLogin from "../components/UserLogin.vue";
import UserRegister from "../components/UserRegister.vue";
import CartPage from "../views/CartPage.vue";
import UserProfile from "../components/UserProfile.vue";
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
    component: CartPage,  
    beforeEnter: (to, from, next) => {
      const userId = localStorage.getItem("user_id");
      if (!userId) {
        // thông báo
        alert("Bạn cần đăng nhập để tiếp tục.");
        next({ name: "login" }); 
      } else {
        next();
      }
    }
  },
  {
    path: "/user/:id", // Đường dẫn cho trang thông tin người dùng
    name: "user-profile",
    component: UserProfile,  
    props: true,  
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
