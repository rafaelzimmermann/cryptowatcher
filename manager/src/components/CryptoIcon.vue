<template>
    <object type="image/svg+xml" :data="icon(currency)" width="32" height="32">
        <img src="/icons/crypto/generic.png" alt="No SVG support" width="32" height="32">
    </object> 
</template>

<script>
export default {
    name: 'CryptoIcon',
    props: {
        currency: {
            type: String,
            required: true
        }
    },
    methods: {
        icon(currency) {
            if (!currency) {
                return '';
            }
            return '/icons/crypto/' + currency.toLowerCase() + '.svg';
        }
    }
}
</script>
