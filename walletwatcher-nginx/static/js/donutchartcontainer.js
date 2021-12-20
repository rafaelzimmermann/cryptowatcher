var sum = (a, b) => { return a + b };

var drawTotals = (chart, options) => {
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
        if (options.display === true && options.text.length > 0) {
            drawTotals(chart, options);
        }
    }
}

Chart.register(centerTitlePlugin);


const DonutChartContainer = {
    name: 'DonutChartContainer',
    extends: VueChartJs.Doughnut,
    props: {
        chartData: {
            default: {
                labels: [],
                datasets: []
            }
        }
    },
    mixins: [VueChartJs.mixins.reactiveProp],
    data: () => ({
        loaded: false,
        options: {
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
                centerTitle: {
                    display: true,
                    text: '',
                    color: 'White'
                }
            }
        }
    }),
    methods: {
        calcBalance: (data) => {
            var total = 0;
            data.datasets.forEach(dataset => {
                total += dataset.data.reduce(sum);
            });
            return "  € " + total.toFixed(2);
        }
    },
    watch: {
        chartData () {
            if (this.chartData && this.chartData.datasets.length > 0 && this.options) {
                this.options.plugins.centerTitle.text = this.calcBalance(this.chartData);
                this.$data._chart.update();
            }
        }
    },
    template: `
        <div class="container">
            <doughnut-chart :chart-data="chartdata" :options="options"/>
        </div>
    `,
    async mounted () {
        this.loaded = true;
        this.renderChart(this.chartData, this.options);
    }
  }

export { DonutChartContainer };