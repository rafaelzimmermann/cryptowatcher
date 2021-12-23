<template>
    <div>
        <header>  
            <div class="pricing-header p-3 pb-md-4 mx-auto text-center">
                <h1 class="display-4 fw-normal">Support CryptoWatcher</h1>
                <p class="fs-5 text-muted">
                    This project rely on support from people like you to make it possible.
                    If you enjoy CryptoWatcher, please consider supporting it.
                </p>
            </div>
        </header>
        <main class="support">
            <div class="row row-cols-1 row-cols-md-3 mb-3 text-center">
                <div class="col">
                    <div class="card mb-4 rounded-3 shadow-sm text-black">
                        <div class="card-header py-3">
                            <h4 class="my-0 fw-normal">BTC</h4>
                        </div>
                        <div class="card-body">
                            <div class="card-body">
                                <qrcode-vue class="img-fluid" value="1NpcgStg75y4UbTGGmRsJrFdDUKsGqWcBw" render-as="svg" width="200px" size="200px"/>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="card mb-4 rounded-3 shadow-sm text-black">
                        <div class="card-header py-3">
                            <h4 class="my-0 fw-normal">ETH</h4>
                        </div>
                        <div class="card-body">
                            <div class="card-body">
                                <qrcode-vue class="img-fluid" value="0x22eb71c0a1D2f4a926Ff5C248DB6B03Af7a069CC" render-as="svg" width="200px" size="200px"/>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="card mb-4 rounded-3 shadow-sm text-black">
                        <div class="card-header py-3">
                            <h4 class="my-0 fw-normal">BNB</h4>
                        </div>
                        <div class="card-body">
                            <div class="card-body">
                                <qrcode-vue class="img-fluid" value="bnb1k2d62md2p3edeu32hm3ke027sw7q603nq7n608" render-as="svg" width="200px" size="200px"/>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="card mb-4 rounded-3 shadow-sm text-black">
                        <div class="card-header py-3">
                            <h4 class="my-0 fw-normal">USDT (ETH network)</h4>
                        </div>
                        <div class="card-body">
                            <qrcode-vue class="img-fluid"  value="0x22eb71c0a1D2f4a926Ff5C248DB6B03Af7a069CC" render-as="svg" width="200px" size="200px"/>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="card mb-4 rounded-3 shadow-sm text-black">
                        <div class="card-header py-3">
                            <h4 class="my-0 fw-normal">Sol</h4>
                        </div>
                        <div class="card-body">
                            <qrcode-vue class="img-fluid"  value="6hB2qFZQpewU2CAC3AheC8fUrnerm6pfaJuntFfhRioQ" render-as="svg" width="200px" size="200px"/>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="card mb-4 rounded-3 shadow-sm text-black">
                        <div class="card-header py-3">
                            <h4 class="my-0 fw-normal">Cardano</h4>
                        </div>
                        <div class="card-body">
                            <qrcode-vue class="img-fluid"  value="Ae2tdPwUPEZJDPj4VsognABCboGwUF2ACUJMbeHT55TpQ97DimoafCVS1xV" render-as="svg" width="200px" size="200px"/>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import QrcodeVue from 'qrcode.vue'
export default {
    name: 'Support',
    components: {QrcodeVue}
};
</script>
