
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
    watch: {
        chartData () {
            if (this.loaded ) {
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
      this.renderChart(this.chartdata, this.options)
    }
  }

export { DonutChartContainer };