

var app = new Vue({
    el: '#app',
    data: {
      transactions: [],
      limit: 25,
      offset: 0
    },
    created:  function() {
      fetch("/v1/transactions?limit=" + this.limit + "&offset=" + this.offset)
        .then(async resp => {
          const data = await resp.json();
          if (resp.ok) {
            this.transactions = data;
          }
        })
    }
  })