-- =====================================================================
-- sales_data_raw.sql
-- DDL for the raw landing table that holds the Mexico FMCG invoice feed.
-- Loaded by an external process (COPY INTO from a stage); never written
-- to by dbt — dbt only reads from this table.
--
-- Source:   Mexico FMCG Retail Sales Customer Inventory (2024)
-- Volume:   100,000 invoices spanning 2024-01-01 to 2024-12-30
-- Grain:    one row per invoice line
-- Schema:   FMCG_RTM.raw.sales_data_raw
-- =====================================================================

CREATE OR REPLACE TABLE FMCG_RTM.raw.sales_data_raw (
    invoice_id          NUMBER(18, 0)   NOT NULL  COMMENT 'Source invoice identifier; unique per row',
    invoice_date        TIMESTAMP_NTZ              COMMENT 'Invoice timestamp; date portion drives the calendar',
    city                VARCHAR(64)                COMMENT 'Store city — Monterrey, CDMX, Guadalajara, Leon, Puebla, Tijuana, Querétaro',
    store_format        VARCHAR(32)                COMMENT 'Store format — Hyper, Super, Express',
    category            VARCHAR(64)                COMMENT 'Product category — Grocery, Home Care, Personal Care, Beverages',
    brand               VARCHAR(64)                COMMENT 'Product brand — Nestle, PepsiCo, Unilever, Bimbo, etc.',
    channel             VARCHAR(32)                COMMENT 'Sales channel — Online, Offline, Omnichannel',
    payment_mode        VARCHAR(32)                COMMENT 'Cash / Card / Wallet / UPI',
    units               NUMBER(10, 0)              COMMENT 'Number of units sold on the invoice line',
    cost_price          NUMBER(20, 10)             COMMENT 'Unit cost in MXN (raw, unrounded)',
    selling_price       NUMBER(20, 10)             COMMENT 'Unit selling price in MXN (raw, unrounded)',
    revenue             NUMBER(20, 10)             COMMENT 'units * selling_price (MXN)',
    cost                NUMBER(20, 10)             COMMENT 'units * cost_price (MXN)',
    margin              NUMBER(20, 10)             COMMENT 'revenue - cost (MXN)',
    "Margin_%"          NUMBER(20, 18)             COMMENT 'margin / revenue; ratio between 0 and 1',
    stock_on_hand       NUMBER(10, 0)              COMMENT 'Units in stock at the time of the invoice',
    reorder_level       NUMBER(10, 0)              COMMENT 'Reorder threshold for the SKU',
    lead_time_days      NUMBER(10, 0)              COMMENT 'Replenishment lead time in days',
    customer_age        NUMBER(10, 1)              COMMENT 'Customer age in years; nulls present in source (~15%)',
    customer_gender     VARCHAR(8)                 COMMENT 'M / F / O / N/A — cleaned to M/F/N/A in staging',
    loyalty_flag        NUMBER(1, 0)               COMMENT '1 = loyalty member, 0 = non-member'
)
COMMENT = 'Raw Mexico FMCG invoice feed — landing zone for dbt staging models';

-- Optional: clustering hint for analytical reads on date + city
-- ALTER TABLE FMCG_RTM.raw.sales_data_raw CLUSTER BY (DATE(invoice_date), city);

-- Bulk load from a Snowflake stage (replace @raw_stage with your stage name):
-- COPY INTO FMCG_RTM.raw.sales_data_raw
--     FROM @raw_stage/sales_data_raw.csv
--     FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);
