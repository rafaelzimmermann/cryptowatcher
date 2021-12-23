CryptoWatcher
========

Track your favorite crypto coin price and your wallet balance.

![image](https://user-images.githubusercontent.com/2369982/132985763-1ed6920c-2a44-442b-bb9d-7373d82a4d2e.png)

Import your tranasctions and manage your wallets. (Work In Progress)

![image](https://user-images.githubusercontent.com/2369982/147010380-da48c3c2-55a4-4330-875c-bdef65d36e78.png)


## Install

### Create .env:
```
ADMIN_USER=admin  
ADMIN_PASSWORD=admin
```

### Configure your wallet assets and prices to watch

```
vi walletwatcher/config.json
```


### Clone this repository on your Docker host, cd into test directory and run compose up:

```
git clone https://github.com/rafaelzimmermann/cryptowatcher.git
cd cryptowatcher
docker-compose up -d
```

Grafana: 
[http://localhost:3000/](http://localhost:3000/d/WJea-ZI7k/crypto-price?orgId=1&from=now-3h&to=now)

Wallet watcher manager:
[http://localhost:1337/](http://localhost:1337/)


To check the available symbols:
```
curl https://api.binance.com/api/v3/exchangeInfo | jq ".symbols[].symbol"
```

## Prerequisites:

* Docker Engine >= 1.13
* Docker Compose >= 1.11

## Containers:

* Prometheus (metrics database) `http://<host-ip>:9090`
* Grafana (visualize metrics) `http://<host-ip>:3000`
* walletwatcher (API that allows user to import transcations csv file and configure wallets)
* manager (API Front-end [WIP]) 

## Setup Grafana

Navigate to `http://<host-ip>:3000` and login with user ***admin*** password ***admin***. You can change the credentials in the compose file or by supplying the `ADMIN_USER` and `ADMIN_PASSWORD` environment variables via .env file on compose up. The config file can be added directly in grafana part like this
```
grafana:
  image: grafana/grafana:5.2.4
  env_file:
    - config

```
and the config file format should have this content
```
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=changeme
GF_USERS_ALLOW_SIGN_UP=false
```
If you want to change the password, you have to remove this entry, otherwise the change will not take effect
```
- grafana_data:/var/lib/grafana
```

Grafana is preconfigured with dashboards and Prometheus as the default data source:

* Name: Prometheus
* Type: Prometheus
* Url: http://prometheus:9090
* Access: proxy

------

## Special Thanks

[Atomic labs]('https://github.com/atomiclabs') for [svg icons](https://github.com/atomiclabs/cryptocurrency-icons/)
