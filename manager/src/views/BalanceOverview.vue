<template>
    <div>
        <div>
            <BalanceDoughnutChart :chartData="chartdata"></BalanceDoughnutChart>
        </div>
        
        <div class="table-responsive" v-if="loaded">
            <table class="table table-dark table-borderless table-sm">
                <thead>
                    <th scope="col">Asset</th>
                    <th scope="col">Ticker</th>
                    <th scope="col">Balance</th>
                    <th scope="col">Value</th>
                </thead>
                <tbody>
                <tr class="table-active" v-for="b in balance" :key="b">
                    <th scope="row">
                        <object type="image/svg+xml" :data="icon(b)" width="32" height="32">
                            <img src="/icons/crypto/generic.png" alt="No SVG support" width="32" height="32">
                        </object>   
                    </th>
                    <td>{{ b.ticker }}</td>
                    <td>{{ b.amount.toFixed(4) }}</td>
                    <td>€ {{ b.value.toFixed(2) }}</td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import '../balance'
import { getSimpleBalance} from '../balance'

export default {
    name: 'BalanceOverview',
    data: () => ({
        balance: [],
        chartdata: {
        labels: [],
        datasets: []
        },
        loaded: false
    }),
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
}
</script>

<style>

</style>