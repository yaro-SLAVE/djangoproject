import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Tasks from '../views/Tasks.vue'
import Tests from '../views/Tests.vue'
import Profile from '../views/Profile.vue'
import Login from '../views/Login.vue'
import Registry from '../views/Registry.vue'
import useUserProfileStore from '@/stores/userProfileStore'
import { storeToRefs } from 'pinia';

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
})

router.beforeEach((to, from, next) => {
  const store = useUserProfileStore()
  
  if (!storeToRefs(store).is_auth.value && to.name !== 'Login' && to.name !== 'Registration') {
    next({ name: "Login" })
  } else {
    next()
  }
})

export default router
