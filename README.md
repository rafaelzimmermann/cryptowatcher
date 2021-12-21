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
* walletwatcher-nginx 

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



## Did you like it? Consider paying me a coffee

| BTC             | Cardano         | Sol             |
| --------------- | --------------- | --------------- |
| <img src="https://user-images.githubusercontent.com/2369982/132985113-aff4d61f-b262-48e8-b998-0c3ae4fee834.png" alt="BTC" width="200"/> | <img src="https://user-images.githubusercontent.com/2369982/143719435-17815999-2df2-4015-a2f2-54a02618cf2a.png" alt="ADA" width="200"/> | <img src="https://user-images.githubusercontent.com/2369982/143735968-1dd9de18-9260-4c9c-9030-f09ea86c8160.png" alt="SOL" width="200"/> |

Based on: [Docker-Compose-Prometheus-and-Grafana](https://github.com/Einsteinish/Docker-Compose-Prometheus-and-Grafana)
