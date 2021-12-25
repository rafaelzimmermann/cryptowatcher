var join = function(values, delimiter) {
    var result = "";
    values.forEach(v => {
        if (!result) {
            result = v;
            return;
        }
        result += delimiter + v;
    });
    return result;
}

var getPrices = async function(tickers) {
    const pricePromise = await fetch("/v1/prices?tickers=" + join(tickers, ",") + "&currency=EUR");
    const priceResp = await pricePromise.json();
    var prices = {}
    for(let index in priceResp) {
        prices[priceResp[index].ticker] = priceResp[index].price;
    }
    return prices;
}

var getSimpleBalance = async function() {
    const response = await fetch("/v1/balance");
    const balance = await response.json();
    var result_1 = {};
    
    var tickers = new Set([]);
    for (let wallet in balance) {
        for (let ticker in balance[wallet]) {
            tickers.add(ticker);
        }
    }
    
    var prices = await getPrices(tickers);

    for (let wallet in balance) {
        for (let ticker in balance[wallet]) {
            if (Object.prototype.hasOwnProperty.call(result_1, ticker) && Object.prototype.hasOwnProperty.call(prices, ticker)) {
                result_1[ticker]["value"] += balance[wallet][ticker]["amount"] * prices[ticker];
                result_1[ticker]["amount"] += balance[wallet][ticker]["amount"];
            } else if (Object.prototype.hasOwnProperty.call(prices, ticker)) {
                result_1[ticker] = {
                    "value": balance[wallet][ticker]["amount"] * prices[ticker],
                    "amount": balance[wallet][ticker]["amount"]
                }
            }
        }
    }

    console.log(result_1)
    var result = [];
    for (var t in result_1) {
        var b = result_1[t];
        b["ticker"] = t;
        result.push(b);
    }
    result.sort((a, b_1) => { return b_1.value - a.value; });
    console.log(result)
    return result;
}

export { getSimpleBalance };