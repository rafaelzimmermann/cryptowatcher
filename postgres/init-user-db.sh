#!/bin/sh
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE walletwatcher TO walletwatcher;


    CREATE SCHEMA IF NOT EXISTS "walletwatcher" ;

    CREATE TABLE IF NOT EXISTS "walletwatcher"."transaction" (
      "id" SERIAL PRIMARY KEY,
      "date" TIMESTAMP NOT NULL,
      "type" INT NOT NULL,
      "wallet" INT NOT NULL,
      "out_amount" BIGINT NULL,
      "out_currency" VARCHAR(10) NULL,
      "fee_amount" BIGINT NULL,
      "fee_currency" VARCHAR(10) NULL,
      "in_amount" BIGINT NULL,
      "in_currency" VARCHAR(10) NULL,
      "txid" VARCHAR(100) NOT NULL) ;

EOSQL