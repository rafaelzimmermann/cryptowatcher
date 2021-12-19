var getSimpleBalance = function() {
    return fetch("/v1/balance")
      .then(response => response.json())
      .then(function(balance) {
          var result = {};
          for (var wallet in balance) {
              for (var ticker in balance[wallet]) {
                  if (result.hasOwnProperty(ticker)) {
                      if (balance[wallet][ticker].hasOwnProperty("EUR")) {
                        result[ticker] += balance[wallet][ticker]["EUR"];
                        result[ticker] = {
                            "value": result[ticker]["value"] + balance[wallet][ticker]["EUR"],
                            "amount": result[ticker]["amount"] + balance[wallet][ticker]["amount"]
                        };
                      }
                  } else if (balance[wallet][ticker].hasOwnProperty("EUR")) {
                      result[ticker] = {
                          "value": balance[wallet][ticker]["EUR"],
                          "amount": balance[wallet][ticker]["amount"]
                      };
                  }
              }
          }
          balance = []
          for (var ticker in result) {
            b = result[ticker];
            b["ticker"] = ticker;
            balance.push(b);
          }
          balance.sort((a, b) => { return b.value - a.value});
          return balance;
      });
}
