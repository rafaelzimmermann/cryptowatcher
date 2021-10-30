CryptoWatcher
========

Track your favorite crypto coin price and your wallet balance.

![image](https://user-images.githubusercontent.com/2369982/132985763-1ed6920c-2a44-442b-bb9d-7373d82a4d2e.png)




## Install

### Create .env:
```
ADMIN_USER=admin  
ADMIN_PASSWORD=admin
```

### Configure your wallet assets and prices to watch

```
vi cryptowatcher/config.json
```


### Clone this repository on your Docker host, cd into test directory and run compose up:

```
git clone https://github.com/rafaelzimmermann/cryptowatcher.git
cd cryptowatcher
docker-compose up -d
```

Open on your browser: 
[http://localhost:3000/](http://localhost:3000/d/WJea-ZI7k/crypto-price?orgId=1&from=now-3h&to=now)


To check the available symbols:
```
curl https://api.binance.com/api/v3/exchangeInfo | jq ".symbols[].symbol"
```

## Prerequisites:

* Docker Engine >= 1.13
* Docker Compose >= 1.11

## Containers:

* Prometheus (metrics database) `http://<host-ip>:9090`
* Prometheus-Pushgateway (push acceptor for ephemeral and batch jobs) `http://<host-ip>:9091`
* Grafana (visualize metrics) `http://<host-ip>:3000`
* cryptowatcher (containers that collect prices)

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

Powered by: 

[<img src="https://user-images.githubusercontent.com/2369982/132985035-7cb35db9-d4db-4cc4-afe6-e609a96958f8.png" width="400" />](https://accounts.binance.com/en/register?ref=200897200)


## Did you like it? Consider paying me a coffee

| BTC             | Cardano         | 
| --------------- | --------------- |
| ![image](https://user-images.githubusercontent.com/2369982/132985113-aff4d61f-b262-48e8-b998-0c3ae4fee834.png) | ![image](https://user-images.githubusercontent.com/2369982/132985145-329632b1-e4d5-4d79-b214-e22c7773c146.png) |

Based on: [Docker-Compose-Prometheus-and-Grafana](https://github.com/Einsteinish/Docker-Compose-Prometheus-and-Grafana)
