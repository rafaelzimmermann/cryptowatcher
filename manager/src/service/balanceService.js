var getSimpleBalance = async function() {
    const response = await fetch("/v1/balance");
    const balance = await response.json();
    var result_1 = {};
    for (var wallet in balance) {
        for (var ticker in balance[wallet]) {
            if (Object.prototype.hasOwnProperty.call(result_1, ticker)) {
                if (Object.prototype.hasOwnProperty.call(balance[wallet][ticker], "EUR")) {
                    result_1[ticker] += balance[wallet][ticker]["EUR"];
                    result_1[ticker] = {
                        "value": result_1[ticker]["value"] + balance[wallet][ticker]["EUR"],
                        "amount": result_1[ticker]["amount"] + balance[wallet][ticker]["amount"]
                    };
                }
            } else if (Object.prototype.hasOwnProperty.call(balance[wallet][ticker], "EUR")) {
                result_1[ticker] = {
                    "value": balance[wallet][ticker]["EUR"],
                    "amount": balance[wallet][ticker]["amount"]
                };
            }
        }
    }
    var result = [];
    for (var t in result_1) {
        var b = result_1[t];
        b["ticker"] = t;
        result.push(b);
    }
    result.sort((a, b_1) => { return b_1.value - a.value; });
    return result;
}

export { getSimpleBalance };