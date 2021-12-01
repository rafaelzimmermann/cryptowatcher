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

const data = {
  labels: ['Red', 'Orange', 'Yellow', 'Green', 'Blue'],
  datasets: [
    {
      label: 'Dataset 1',
      data: [10, 20, 30, 40, 50],
      backgroundColor: COLORS,
    }
  ]
};

const config = {
  type: 'doughnut',
  data: data,
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

const ctx = document.getElementById('balance').getContext('2d');
const myChart = new Chart(ctx, config);



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
