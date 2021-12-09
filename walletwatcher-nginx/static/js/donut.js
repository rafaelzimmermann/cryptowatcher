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
    borderColor: '#292929',
    offset: 2,
    cutout: "97%",
    plugins: {
      legend: {
        display: false
      },
      centerTitle: {
        display: true,
        text: '',
        color: 'White'
      }
    }
  },
};

function drawTotals(chart, options) {
  let width = chart.chartArea.width;
  let height = chart.chartArea.height;
  let ctx = chart.ctx;

  ctx.restore();
  let fontSize = (height / 130).toFixed(2);
  ctx.font = fontSize + "em Roboto,sans-serif";
  ctx.fillStyle = options.color;
  ctx.textBaseline = "middle";

  let textX = Math.round((width - ctx.measureText(options.text).width) * 0.5);
  let textY = height / 2;
  ctx.fillText(options.text, textX, textY);
  ctx.save();
}

var centerTitlePlugin = {
  id: 'centerTitle',
  beforeDraw: function(chart, args, options) {
    if (options.display === true) {
      drawTotals(chart, options);
    }
  }
}

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
    total = 0;
    tickers.forEach((t) => {
        balances.push(balance[t]);
        total += balance[t];
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
    config.options.plugins.centerTitle.text = "€" + total.toFixed(2);
    Chart.register(centerTitlePlugin)
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
