import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Tasks from '../views/Tasks.vue'
import Tests from '../views/Tests.vue'
import Profile from '../views/Profile.vue'
import Login from '../views/Login.vue'
import Registry from '../views/Registry.vue'

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

export default router
