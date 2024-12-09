import { createApp } from 'vue';
import { createPinia } from 'pinia';
import "bootstrap/dist/css/bootstrap.css";
import VueMathJax from 'vue-mathjax-next';

import "bootstrap";

import App from './App.vue';
import router from './router';

const app = createApp(App);
app.use(createPinia());
app.use(VueMathJax);
app.use(router);

app.mount('#app');