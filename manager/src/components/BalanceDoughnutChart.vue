<template>
  <DoughnutChart ref="doughtnutRef" :chartData="chartData" @chart:render="handleChartRender" :options="options" />
</template>

<script>
import { DoughnutChart } from 'vue-chart-3';
import { defineComponent, ref, onMounted } from 'vue';

import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)
  
var centerTitlePlugin = {
    id: 'centerTitle',
    beforeDraw: function(chart, args, options) {
      console.log(chart)
      var calcBalance = (datasets) => {
        var total = 0;
        datasets.forEach(dataset => {
            if (dataset.data) {
              total += dataset.data.reduce((a , b) => a + b);
            }
        });
        if (total == 0) {
          return;
        }
        return "  € " + total.toFixed(2);
      };
      var drawTotals = (chart, options) => {
        var text = calcBalance(chart.data.datasets);
        
        if (!text) {
          return;
        }

        let width = chart.chartArea.width;
        let height = chart.chartArea.height;
        let ctx = chart.ctx;
        
      
        ctx.restore();
        let fontSize = (height / 130).toFixed(2);
        ctx.font = fontSize + "em Roboto,sans-serif";
        ctx.fillStyle = options.color;
        ctx.textBaseline = "middle";
      
        let textX = Math.round((width - ctx.measureText(text).width) * 0.5);
        let textY = height / 2;
        ctx.fillText(text, textX, textY);
        ctx.save();
      }
      drawTotals(chart, options);
    }
}

Chart.register(centerTitlePlugin);

export default defineComponent({
  name: 'BalanceDoughnutChart',
  components: { DoughnutChart },
  setup() {
    const chartData = ref({
      labels: ['Paris', 'Nîmes', 'Toulon', 'Perpignan', 'Autre'],
      datasets: [
        {
          data: [30, 40, 60, 70, 5],
          backgroundColor: ['#77CEFF', '#0079AF', '#123E6B', '#97B0C4', '#A5C8ED'],
        },
      ],
    });

    const options = ref({
      responsive: true,
      aspectRatio: 1,
      borderColor: '#292929',
      offset: 2,
      cutout: "97%",
      maintainAspectRatio: false,
      layout: {
        padding: 20
      },
      plugins: {
        legend: {
          display: false
        },
        title: {
          display: false,
        },
        centerTitle: {
          display: true,
          color: 'White'
        }
      },
    });

    const doughtnutRef = ref();
    onMounted(() => {
    });

    // Chart instance is accessible on events too
    function handleChartRender(chart) {
      console.log(chart);
    }

    return { chartData, doughtnutRef, handleChartRender, options };
  },
});
</script>