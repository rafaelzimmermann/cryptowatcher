<template>
    <div v-if="currency" class="row no-gutters align-items-center">
        <picture class="col-auto">
            <crypto-icon :currency="currency" class="mr-3" />
        </picture>
        <div class="col v-stack gap-1">
            <div class="">
                {{ currency }}
            </div>
            <div v-if="amount">{{ Number(amount).toFixed(4) }}</div>
        </div>
        
    </div>
</template>

<script>
import CryptoIcon from './CryptoIcon.vue';
export default {
  components: { CryptoIcon },
    name: 'IconAndPrice',
    props: {
        currency: {
            type: String,
            required: false
        },
        amount: {
            type: Number,
            required: false
        }
    }
};
</script>