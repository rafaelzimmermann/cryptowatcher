var app = new Vue({
    el: '#app',
    data: {
      balance: [],
    },
    methods: {
        icon(balance) {
            return '/icons/' + balance.ticker.toLowerCase() + '.svg';
        }
    },
    created:  function() {
      getSimpleBalance()
        .then(resp => {
          this.balance = resp;
        });
    }
  })