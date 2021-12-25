<template>
    <div class="container pt-3">
        <ConfigurationForm :configuration="configuration" />
    </div>
</template>
<script>
export default {
    name: 'Configuration',
    data: () => ({
        configuration: {
            currency: "EUR",
            manual: true,
            wallets: [{
                name: "binance"
            }],
            maunualPortifolio: {}

        }
    }),
    
}
</script>
