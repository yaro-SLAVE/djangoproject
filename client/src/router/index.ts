import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Tasks from '../views/Tasks.vue'
import Tests from '../views/Tests.vue'
import Profile from '../views/Profile.vue'
import Login from '../views/Login.vue'
import Registry from '../views/Registry.vue'
import useUserProfileStore from '@/stores/userProfileStore'
import { storeToRefs } from 'pinia';
import { toValue, type RefSymbol } from '@vue/reactivity'
import type { User } from "@/customTypes"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Home, name: 'Main' },
    { path: '/tasks', component: Tasks, name: 'Tasks' },
    { path: '/tests', component: Tests, name: 'Tests' },
    { path: '/profile', component: Profile, name: 'Profile' },
    { path: '/login', component: Login, name: 'Login' },
    { path: '/registration', component: Registry, name: 'Registration' },
  ]
});

router.beforeEach((to, from, next) => {
  const { is_auth } = storeToRefs(useUserProfileStore());

  if (!is_auth.value && to.name !== 'Login' && to.name !== 'Registration') {
    next({ name: 'Login' });
  } else if (is_auth.value && (to.name === 'Login' || to.name === 'Registration')) {
    next({ name: 'Profile' });
  } else {
    next();
  }
})

export default router;