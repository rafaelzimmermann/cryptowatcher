var app = new Vue({
    el: '#app',
    data: {
      balance: {},
    },
    methods: {
        icon(ticker) {
            return '/icons/' + ticker.toLowerCase() + '.svg';
        }
    },
    created:  function() {
      getSimpleBalance()
        .then(resp => {
            this.balance = resp;
        });
    }
  })