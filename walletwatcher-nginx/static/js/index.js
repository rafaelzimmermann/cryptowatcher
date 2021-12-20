import { getSimpleBalance } from './balance.js';
import {DonutChartContainer} from  './donutchartcontainer.js';


var app = new Vue({
    el: '#app',
    data: {
      balance: [],
      chartdata: {
        labels: [],
        datasets: []
      },
      loaded: false
    },
    components: {DonutChartContainer},
    methods: {
        icon(balance) {
            return '/icons/crypto/' + balance.ticker.toLowerCase() + '.svg';
        }
    },
    created: function() {
      getSimpleBalance()
        .then(resp => {
          
          this.balance = resp;
          this.chartdata = {
            labels: this.balance.map(b => { return b.ticker }),
            datasets: [{
                label: 'Balance',
                backgroundColor: '#fff',
                data: this.balance.map(b => {return b.value})
            }]
          }
          this.loaded = true;
        });
    }
  })