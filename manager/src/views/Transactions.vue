<template>
    <table class="table table-dark table-striped">
        <thead>
            <tr>
            <th scope="col">Date</th>
            <th scope="col">In</th>
            <th scope="col">Out</th>
            <th scope="col">Fee</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="t in transactions" :key="t">
                <th scope="row">
                      {{ t.date }}
                </th>
                <td class="align-middl">
                    <IconAndPrice :currency="t.in_currency" :amount="t.in_amount_float"/>
                </td>
                <td class="align-middl">
                    <IconAndPrice :currency="t.out_currency" :amount="t.out_amount_float"/>
                </td>
                <td class="align-middl">
                    <IconAndPrice :currency="t.fee_currency" :amount="t.fee_amount_float"/>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import { IconAndPrice } from '../components/IconAndPrice.vue';
import { getTransactions } from '../service/transactionService'

export default {
    name: 'Transactions',
    components: { IconAndPrice },
    data: () => ({
        transactions: [],
        limit: 25,
        offset: 0
    }),
    created: function() {
        getTransactions(this.limit, this.offset)
            .then(transactions => {
                this.transactions = transactions;
            });
    }
}
</script>

<style>
</style>