import Vue from 'vue';
import VueRouter from 'vue-router';

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import App from './App.vue';
import Home from './components/Home.vue';
import About from './components/About.vue';
import Dashboard from './components/Dashboard.vue';

Vue.use(VueRouter);

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/dashboard', component: Dashboard }
];

const router = new VueRouter({
  routes,
  mode: 'history'
});

new Vue({
  el: '#app',
  router,
  render: (h) => h(App),
}).$mount('#app');
