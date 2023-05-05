import { createWebHistory, createRouter } from "vue-router";
import ChatUI from "../components/ChatUI.vue";

const routes = [
  {
    path: "/",
    name: "ChatUI",
    component: ChatUI,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;