import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import UserLogin from "../components/UserLogin.vue";
import UserRegister from "../components/UserRegister.vue";

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
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/product/:id",
    name: "product-detail",
    component: () => import("../views/ProductDetail.vue")
  }
  
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
