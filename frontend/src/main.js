// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import VuePromiseBtn from 'vue-promise-btn';
import Sticky from 'vue-sticky-directive';
import App from './App';
import router from './router';

const config = require('./config');

Vue.config.productionTip = false;
Vue.use(VuePromiseBtn, {});

const shared = {
  rootUrl: config.rootUrl,
};

shared.install = () => {
  Object.defineProperty(Vue.prototype, '$globalData', {
    get() {
      return shared;
    },
  });
};

Vue.use(Sticky);

Vue.http.options.root = config.rootUrl;
Vue.http.interceptors.push((request) => {
  request.headers.set('X-Access-Token', Vue.cookie.get(config.authTokenCookie));
  return (response) => {
    if (response.status === 404) {
      window.vm.$snotify.error('404', { timeout: 0 });
    }
  };
});

Vue.prototype.$eventHub = new Vue(); // Global event bus

// eslint-disable-next-line
const vm = new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
window.vm = vm;
