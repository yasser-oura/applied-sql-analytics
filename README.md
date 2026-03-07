# Applied SQL Analytics

A collection of **25 SQL analytics queries** built on a mock e-commerce dataset, covering joins, aggregations, window functions, CTEs, and cohort analysis — all executed against a PostgreSQL database via Python.

## ER Schema

[ER Schema]
<img width="700" height="692" alt="image" src="https://github.com/user-attachments/assets/d4cde37b-f596-47bc-b47a-b947e3548aec" />


### Tables

| Table | Primary Key | Description |
|---|---|---|
| **orders** | `order_id` | Core orders table with amount, channel, shipping, and coupon info |
| **customers** | `customer_id` | Customer profiles with tier and signup date |
| **countries** | `country_code` | Country reference data with currency and region |
| **coupons** | `coupon_code` | Discount coupons with validity and usage rules |
| **order_status_history** | `history_id` | Status change log for each order |

## Queries Overview

| # | Topic |
|---|---|
| Q1–Q5 | **INNER JOINs** — orders with country names, customer tiers, coupon details, multi-table joins, status history |
| Q6–Q9 | **LEFT JOINs** — countries with zero orders, customers with no orders, optional coupon info, coupon usage counts |
| Q10–Q14 | **Aggregations** — revenue per region, avg order by tier, top spenders, discount totals, orders per channel/region |
| Q15–Q18 | **Filtering & Subqueries** — cross-country orders, above-average customers, status change counts, expired coupons |
| Q19–Q22 | **Window Functions & CTEs** — top channel per region, customer value classification, country ranking, time between status changes |
| Q23–Q25 | **Business Reports** — monthly report, signup speed analysis, cohort analysis |

## Setup

### Prerequisites

- Python 3
- PostgreSQL database with the schema above populated
- `psycopg2` and `python-dotenv`

### Install dependencies

```bash
pip install psycopg2-binary python-dotenv
```

### Configure environment

Create a `.env` file in the project root:

```
DB_HOST=your_host
DB_PORT=5432
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
```

### Run

```bash
python main.py
```

This runs all 25 queries and prints the results to the console.

## Files

| File | Description |
|---|---|
| `main.py` | Python script that connects to PostgreSQL and runs all queries |
| `sprint3_answers.sql` | Standalone SQL file with all 25 queries and comments |
