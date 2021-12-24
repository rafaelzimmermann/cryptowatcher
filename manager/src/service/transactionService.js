var getTransactions = async function(limit, offset) {
    let params = {
        "limit": limit,
        "offset": offset
    }
    var host = window.location.protocol + "//" + window.location.host;
    let transactionsEndpoint = new URL(host + "/v1/transactions");
    for (let k in params) {
        transactionsEndpoint.searchParams.append(k, params[k]);
    }
    const response = await fetch(transactionsEndpoint);
    return await response.json();
};

export { getTransactions };