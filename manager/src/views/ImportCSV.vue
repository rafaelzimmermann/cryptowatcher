<template>
    <div class="container pt-3">
        <div class="row">
            <div class="col"></div>
            <div class="col-6">
                <form id="csv-upload">
                <div class="row g-1">
                    <div class="form-check form-check-inline pt-3">
                        <input class="form-check-input" type="radio" name="fileType" id="binace-radio" value="binance" v-model="fileType">
                        <label class="form-check-label" for="binace-radio">
                            <img src="/icons/wallet/binance.svg" height="32px" width="32px"/>
                            Binance
                        </label>
                    </div>
                    <div class="form-check form-check-inline pt-3">
                        <input class="form-check-input" type="radio" name="fileType" id="cryptocom-radio" value="cryptocom" v-model="fileType">
                        <label class="form-check-label" for="cryptocom-radio">
                            <img src="/icons/wallet/cryptocom.svg" height="32px" width="32px"/>
                            Crypto.com
                        </label>
                    </div>
                    <div class="form-check form-check-inline pt-3">
                        <input class="form-check-input" type="radio" name="fileType" id="daedalu-radio" value="daedalus" v-model="fileType">
                        <label class="form-check-label" for="daedalu-radio">
                            <img src="/icons/wallet/daedalus.svg" height="32px" width="32px"/>
                            Daedalus
                        </label>
                    </div>
                    <div class="form-check form-check-inline pt-3">
                        <input class="form-check-input" type="radio" name="fileType" id="exodus-radio" value="exodus" v-model="fileType">
                        <label class="form-check-label" for="exodus-radio">
                            <img src="/icons/wallet/exodus.svg" height="32px"/>
                        </label>
                    </div>

                </div>
                <div class="row g-2 pt-3">
                    <div class="col-auto">
                        <input type="file" class="form-control" id="file-input" @change="selectedFile" ref="file"/>
                    </div>
                    <div class="col-auto">
                        <button id="upload-button" type="submit" class="btn btn-primary mb-3" @click="submit">Import</button>
                    </div>
                </div>
                
                </form>

            </div>
            <div class="col">
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ImportCSV',
    data: () => ({
        fileType: "binance"
    }),
    methods: {
        'submit': function(e) {
            e.preventDefault();
            let formData = new FormData();
            var inputFile = e.target.form.querySelector("input[type=file]");
            formData.append('file', inputFile.files[0]);
            fetch('/v1/wallet/' + this.fileType, {
                method: "POST",
                body: formData
            }).catch(console.log);
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
    margin: 40px 0 0;
}
ul {
    list-style-type: none;
    padding: 0;
}
li {
    display: inline-block;
    margin: 0 10px;
}
a {
    color: #42b983;
}
</style>
