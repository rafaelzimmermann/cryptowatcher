CryptoWatch
========

Track your favorite crypto coin price and your wallet balance.

![image](https://user-images.githubusercontent.com/2369982/132984579-8abd9f1e-cfb7-455c-86d4-6544cd61f68d.png)


## Install

### Create .env:
```
ADMIN_USER=admin  
ADMIN_PASSWORD=admin
```

### Clone this repository on your Docker host, cd into test directory and run compose up:

```
git clone https://github.com/rafaelzimmermann/cryptowatch.git
cd cryptowatch
docker-compose up -d
```

### Configure your wallet assets and prices to watch

```
vi cryptowatch/config.json
```

To check the available symbols:
```
curl https://api.binance.com/api/v3/exchangeInfo | jq ".symbols[].symbol"
```

[Prices grafana dashboard](http://localhost:3000/d/WJea-ZI7k/crypto-price?orgId=1&from=now-3h&to=now)

## Prerequisites:

* Docker Engine >= 1.13
* Docker Compose >= 1.11

## Containers:

* Prometheus (metrics database) `http://<host-ip>:9090`
* Prometheus-Pushgateway (push acceptor for ephemeral and batch jobs) `http://<host-ip>:9091`
* Grafana (visualize metrics) `http://<host-ip>:3000`
* cryptowatch (containers that collect prices)

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





Based on: [Docker-Compose-Prometheus-and-Grafana](https://github.com/Einsteinish/Docker-Compose-Prometheus-and-Grafana)
