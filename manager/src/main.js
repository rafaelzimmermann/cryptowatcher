import { createApp } from 'vue'
import App from './App.vue'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import router from './router'

import './assets/css/base.css';
import BalanceDoughnutChart from './components/BalanceDoughnutChart.vue'

createApp(App)
    .use(router)
    .component('BalanceDoughnutChart', BalanceDoughnutChart)
    .mount('#app')
