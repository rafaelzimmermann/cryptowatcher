const DATA_COUNT = 5;
const NUMBER_CFG = {count: DATA_COUNT, min: 0, max: 100};

const COLORS = [
  '#4dc9f6',
  '#f67019',
  '#f53794',
  '#537bc4',
  '#acc236',
  '#166a8f',
  '#00a950',
  '#58595b',
  '#8549ba'
];

var config = {
  type: 'doughnut',
  options: {
    responsive: true,
    aspectRatio: 1,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: 'White'
        }
      },
      title: {
        display: true,
        text: 'Balance',
        color: 'White'
      }
    }
  },
};

var getSimpleBalance = function() {
    return fetch("/v1/balance")
            .then(response => response.json())
            .then(function(balance) {
                var result = {};
                for (var wallet in balance) {
                    for (var ticker in balance[wallet]) {
                        if (result.hasOwnProperty(ticker)) {
                            result[ticker] += balance[wallet][ticker]["EUR"];
                        } else {
                            result[ticker] = balance[wallet][ticker]["EUR"];
                        }
                    }
                }
                return result;
            });
}

var updateChart = function(balance) {
    tickers = Object.keys(balance);
    balances = [];
    tickers.forEach((t) => {
        balances.push(balance[t]);
    });
    const data = {
      labels: tickers,
      datasets: [
        {
          label: 'Balance',
          data: balances,
          backgroundColor: COLORS,
        }
      ]
    };
    config.data = data;
    const ctx = document.getElementById('balance').getContext('2d');
    const myChart = new Chart(ctx, config);
}

getSimpleBalance()
    .then(updateChart);

const actions = [
  {
    name: 'Randomize',
    handler(chart) {
      chart.data.datasets.forEach(dataset => {
        dataset.data = Utils.numbers({count: chart.data.labels.length, min: 0, max: 100});
      });
      chart.update();
    }
  },
  {
    name: 'Add Dataset',
    handler(chart) {
      const data = chart.data;
      const newDataset = {
        label: 'Dataset ' + (data.datasets.length + 1),
        backgroundColor: [],
        data: [],
      };

      for (let i = 0; i < data.labels.length; i++) {
        newDataset.data.push(Utils.numbers({count: 1, min: 0, max: 100}));

        const colorIndex = i % Object.keys(Utils.CHART_COLORS).length;
        newDataset.backgroundColor.push(Object.values(Utils.CHART_COLORS)[colorIndex]);
      }

      chart.data.datasets.push(newDataset);
      chart.update();
    }
  },
  {
    name: 'Add Data',
    handler(chart) {
      const data = chart.data;
      if (data.datasets.length > 0) {
        data.labels.push('data #' + (data.labels.length + 1));

        for (let index = 0; index < data.datasets.length; ++index) {
          data.datasets[index].data.push(Utils.rand(0, 100));
        }

        chart.update();
      }
    }
  },
  {
    name: 'Hide(0)',
    handler(chart) {
      chart.hide(0);
    }
  },
  {
    name: 'Show(0)',
    handler(chart) {
      chart.show(0);
    }
  },
  {
    name: 'Hide (0, 1)',
    handler(chart) {
      chart.hide(0, 1);
    }
  },
  {
    name: 'Show (0, 1)',
    handler(chart) {
      chart.show(0, 1);
    }
  },
  {
    name: 'Remove Dataset',
    handler(chart) {
      chart.data.datasets.pop();
      chart.update();
    }
  },
  {
    name: 'Remove Data',
    handler(chart) {
      chart.data.labels.splice(-1, 1); // remove the label first

      chart.data.datasets.forEach(dataset => {
        dataset.data.pop();
      });

      chart.update();
    }
  }
];
