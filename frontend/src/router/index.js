import Vue from 'vue';
import Router from 'vue-router';

import BootstrapVue from 'bootstrap-vue';
import VueResource from 'vue-resource';
import { fas } from '@fortawesome/free-solid-svg-icons';

import { library as faLibrary } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Snotify, { SnotifyPosition } from 'vue-snotify';
import VueLodash from 'vue-lodash';
import Meta from 'vue-meta';

import 'vue-snotify/styles/material.scss';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';
import Auth from '@/components/Auth/utils';

import LyricsQuiz from '@/components/LyricsQuiz';

const VueCookie = require('vue-cookie');

const config = require('./../config');

faLibrary.add(fas);
Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.use(Router);
Vue.use(BootstrapVue);
Vue.use(VueResource);
Vue.use(Meta);
Vue.use(VueCookie);

Vue.use(VueLodash, { name: '_' });

Vue.http.options.root = config.rootUrl;
Vue.http.interceptors.push((request) => {
  request.headers.set('X-Access-Token', Vue.cookie.get(config.authTokenCookie));
});

Vue.use(Auth);

Vue.use(Snotify, {
  toast: {
    position: SnotifyPosition.rightTop,
  },
});

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: LyricsQuiz,
    },
  ],
});
