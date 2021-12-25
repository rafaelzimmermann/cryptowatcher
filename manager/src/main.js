import { createApp } from 'vue'
import App from './App.vue'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import router from './router'

import './assets/css/base.css';
import BalanceDoughnutChart from './components/BalanceDoughnutChart.vue'
import CryptoIcon from './components/CryptoIcon.vue';
import IconAndPrice from './components/IconAndPrice.vue';
import ConfigurationForm from './components/ConfigurationForm.vue'

const app = createApp(App);
app.use(router);

app.component('BalanceDoughnutChart', BalanceDoughnutChart);
app.component('IconAndPrice', IconAndPrice);
app.component('CryptoIcon', CryptoIcon);
app.component('ConfigurationForm', ConfigurationForm);
app.mount('#app');
