<template>
    <form id="form-config">
            <div class="row p-3">
                <div class="col"></div>
                <div class="col-5">
                        <div class="form-group">
                            <label for="exampleFormControlSelect1">Select currency:</label>
                            <select class="form-control" id="exampleFormControlSelect1" v-model="config.currency">
                                <option>EUR</option>
                                <option>USDT</option>
                            </select>
                        </div>
                </div>
                <div class="col">
                </div>
            </div>
            <div class="row p-3">
                <div class="col"></div>
                <div class="col-5">
                        <div class="form-group">
                            <div>
                                <label for="inlineRadioOptions">Portifolio input:</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="radio" name="portfolioInput" id="portfolioInputManual" value="true" v-model="config.manual">
                                <label class="form-check-label" for="inlineRadio1">Manual</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="radio" name="portfolioInput" id="portfolioInputAutomatic" value="false" v-model="config.manual">
                                <label class="form-check-label" for="inlineRadio2">Automatic (CSV Import)</label>
                            </div>
                        </div>
                </div>
                <div class="col">
                </div>
            </div>
            <div v-if="config.manual">
                <div class="row p-3" v-for="wallet in config.wallets" :key="wallet">
                    <div class="col"></div>
                    <div class="col-5">
                        <div class="form-group">
                            <div>
                                <label for="inlineRadioOptions">Wallet:</label>
                            </div>
                            <div class="form-check form-check-inline pt-3">
                                <input class="form-check-input" type="radio" name="wallet-name" id="binace-radio" value="binance" v-model="wallet.name">
                                <label class="form-check-label" for="binace-radio">
                                    <img src="/icons/wallet/binance.svg" height="32px" width="32px"/>
                                    Binance
                                </label>
                            </div>
                            <div class="form-check form-check-inline pt-3">
                                <input class="form-check-input" type="radio" name="wallet-name" id="cryptocom-radio" value="cryptocom" v-model="wallet.name">
                                <label class="form-check-label" for="cryptocom-radio">
                                    <img src="/icons/wallet/cryptocom.svg" height="32px" width="32px"/>
                                    Crypto.com
                                </label>
                            </div>
                            <div class="form-check form-check-inline pt-3">
                                <input class="form-check-input" type="radio" name="wallet-name" id="daedalu-radio" value="daedalus" v-model="wallet.name">
                                <label class="form-check-label" for="daedalu-radio">
                                    <img src="/icons/wallet/daedalus.svg" height="32px" width="32px"/>
                                    Daedalus
                                </label>
                            </div>
                            <div class="form-check form-check-inline pt-3">
                                <input class="form-check-input" type="radio" name="wallet-name" id="exodus-radio" value="exodus" v-model="wallet.name">
                                <label class="form-check-label" for="exodus-radio">
                                    <img src="/icons/wallet/exodus.svg" height="32px"/>
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                    </div>
                </div>
            </div>
            <div class="row p-3">
                <div class="col"></div>
                <div class="col-5">
                    <div class="col-auto">
                        <button id="save-button" type="submit" class="btn btn-primary mb-3" @click="submit">Save</button>
                    </div>
                </div>
                <div class="col">
                </div>
            </div>
        </form>
</template>

<script>
export default {
    name: 'ConfigurationForm',
    props: {
        configuration: {
            type: Object,
            required: true
        }
    },
    data: () => ({
        config: this.configuration
    }),
    methods: {
        'submit': function(e) {
            e.preventDefault();
            fetch('/v1/configuration' + this.fileType, {
                method: "POST",
                body: e.target.form
            }).catch(console.log);
        }
    }
}
</script>
