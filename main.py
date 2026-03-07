import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
print("HOST:", os.getenv("DB_HOST"))
print("USER:", os.getenv("DB_USER"))
print("PASS:", os.getenv("DB_PASSWORD"))
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", 5432),
    dbname=os.getenv("DB_NAME", "postgres"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)


def run_query(label, query):
    """Run a SQL query and print results."""
    print(f"\n{'='*60}")
    print(f"  {label}")
    print('='*60)
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(dict(row))
        else:
            print("No results.")


# ─── Queries ──────────────────────────────────────────────────────────────────

Q1 = """
SELECT order_id, order_date, country_name, order_amount
FROM orders o
INNER JOIN countries c ON o.country_code = c.country_code;
"""

Q2 = """
SELECT o.order_id, o.customer_id, c.tier, o.order_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;
"""

Q3 = """
SELECT o.order_id, o.order_amount, o.coupon_code, c.discount_percent
FROM orders o
INNER JOIN coupons c ON o.coupon_code = c.coupon_code
WHERE o.coupon_code IS NOT NULL;
"""

Q4 = """
SELECT o.order_id, coun.country_name, cu.tier, o.order_amount
FROM orders o
INNER JOIN countries coun ON o.country_code = coun.country_code
INNER JOIN customers cu ON o.customer_id = cu.customer_id;
"""

Q5 = """
SELECT order_id, status, changed_at
FROM order_status_history
WHERE order_id = 'ORD-1004'
ORDER BY changed_at;
"""

Q6 = """
SELECT c.country_name, COUNT(o.order_id) AS order_count
FROM countries c
LEFT JOIN orders o ON o.country_code = c.country_code
GROUP BY c.country_name;
"""

Q7 = """
SELECT c.customer_id, c.home_country, c.tier, c.signup_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL;
"""

Q8 = """
SELECT o.order_id, o.order_amount, o.coupon_code, c.discount_percent
FROM orders o
LEFT JOIN coupons c ON o.coupon_code = c.coupon_code;
"""

Q9 = """
SELECT c.coupon_code, c.is_active, COUNT(o.coupon_code) AS times_used
FROM coupons c
LEFT JOIN orders o ON o.coupon_code = c.coupon_code
GROUP BY c.coupon_code, c.is_active
ORDER BY times_used;
"""

Q10 = """
SELECT c.region, SUM(o.order_amount) AS total_revenue, COUNT(o.order_id) AS order_count
FROM orders o
INNER JOIN countries c ON o.country_code = c.country_code
GROUP BY c.region
ORDER BY total_revenue DESC;
"""

Q11 = """
SELECT c.tier, ROUND(AVG(o.order_amount), 2) AS avg_order_amount, COUNT(o.order_id) AS order_count
FROM orders o
INNER JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.tier;
"""

Q12 = """
SELECT o.customer_id, c.tier, coun.country_name, SUM(o.order_amount) AS total_spending
FROM customers c
INNER JOIN countries coun ON coun.country_code = c.home_country
INNER JOIN orders o ON o.customer_id = c.customer_id
GROUP BY o.customer_id, c.tier, coun.country_name
ORDER BY total_spending DESC
LIMIT 5;
"""

Q13 = """
SELECT c.coupon_code, COUNT(o.coupon_code) AS times_used,
       ROUND(SUM(o.order_amount * c.discount_percent / 100), 2) AS total_discount_given
FROM coupons c
INNER JOIN orders o ON o.coupon_code = c.coupon_code
GROUP BY c.coupon_code;
"""

Q14 = """
SELECT o.channel, c.region, COUNT(o.order_id) AS order_count
FROM countries c
INNER JOIN orders o ON o.country_code = c.country_code
WHERE o.channel IS NOT NULL
GROUP BY o.channel, c.region;
"""

Q15 = """
SELECT o.order_id, o.customer_id, c.home_country, o.country_code AS order_country, o.order_amount
FROM orders o
INNER JOIN customers c ON c.customer_id = o.customer_id
WHERE o.country_code != c.home_country;
"""

Q16 = """
SELECT c.customer_id, c.tier, ROUND(AVG(o.order_amount), 2) AS avg_amount,
       (SELECT ROUND(AVG(order_amount), 2) FROM orders) AS overall_avg
FROM customers c
INNER JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.tier
HAVING AVG(o.order_amount) > (SELECT ROUND(AVG(order_amount), 2) FROM orders);
"""

Q17 = """
SELECT o1.order_id, o1.order_amount, COUNT(o2.changed_at) AS num_status_changes
FROM orders o1
INNER JOIN order_status_history o2 ON o2.order_id = o1.order_id
GROUP BY o1.order_id, o1.order_amount
ORDER BY num_status_changes DESC;
"""

Q18 = """
SELECT o.order_id, o.order_date, c.coupon_code, c.valid_until
FROM orders o
INNER JOIN coupons c ON c.coupon_code = o.coupon_code
WHERE o.order_date > c.valid_until;
"""

Q19 = """
WITH channel_counts AS (
  SELECT c.region, o.channel, COUNT(o.order_id) AS order_count,
         RANK() OVER (PARTITION BY c.region ORDER BY COUNT(o.order_id) DESC) AS channel_rank
  FROM orders o
  INNER JOIN countries c ON o.country_code = c.country_code
  WHERE o.channel IS NOT NULL
  GROUP BY c.region, o.channel
)
SELECT region, channel, order_count
FROM channel_counts
WHERE channel_rank = 1
ORDER BY region;
"""

Q20 = """
WITH customer_spending AS (
  SELECT c.customer_id, c.tier, ROUND(SUM(o.order_amount), 2) AS total_spent,
    CASE
      WHEN ROUND(SUM(o.order_amount), 2) > 1000 THEN 'high_value'
      WHEN ROUND(SUM(o.order_amount), 2) BETWEEN 500 AND 1000 THEN 'medium_value'
      ELSE 'low_value'
    END AS value_class
  FROM customers c
  INNER JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id, c.tier
)
SELECT * FROM customer_spending;
"""

Q21 = """
SELECT o.order_id, c.country_name, o.order_amount,
       RANK() OVER (PARTITION BY c.country_name ORDER BY o.order_amount DESC) AS country_rank,
       COUNT(o.order_id) OVER (PARTITION BY c.country_name) AS country_total_orders
FROM orders o
INNER JOIN countries c ON o.country_code = c.country_code;
"""

Q22 = """
WITH status_times AS (
  SELECT order_id, changed_at,
         LAG(changed_at) OVER (PARTITION BY order_id ORDER BY changed_at) AS prev_changed_at
  FROM order_status_history
)
SELECT order_id, COUNT(changed_at) AS num_changes,
       ROUND(AVG(EXTRACT(EPOCH FROM (changed_at - prev_changed_at)) / 3600), 2) AS avg_hours_between_changes
FROM status_times
WHERE prev_changed_at IS NOT NULL
GROUP BY order_id
ORDER BY avg_hours_between_changes DESC;
"""

Q23 = """
SELECT
    TO_CHAR(o.order_date, 'YYYY-MM') AS month,
    COUNT(*) AS total_orders,
    ROUND(SUM(o.order_amount), 2) AS total_revenue,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    COUNT(o.coupon_code) AS coupon_orders,
    ROUND(AVG(o.order_amount), 2) AS avg_order_amount,
    ROUND(SUM(CASE WHEN f.first_month = TO_CHAR(o.order_date, 'YYYY-MM')
              THEN o.order_amount ELSE 0 END), 2) AS new_customer_revenue,
    ROUND(SUM(CASE WHEN f.first_month != TO_CHAR(o.order_date, 'YYYY-MM')
              THEN o.order_amount ELSE 0 END), 2) AS returning_customer_revenue
FROM orders o
JOIN (
    SELECT customer_id, TO_CHAR(MIN(order_date), 'YYYY-MM') AS first_month
    FROM orders GROUP BY customer_id
) f ON o.customer_id = f.customer_id
GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')
ORDER BY month;
"""

Q24 = """
WITH first_orders AS (
    SELECT customer_id, MIN(order_date) AS first_order_date
    FROM orders GROUP BY customer_id
)
SELECT
    CASE WHEN fo.first_order_date::date - cu.signup_date <= 30
         THEN 'fast' ELSE 'slow' END AS signup_speed,
    COUNT(DISTINCT cu.customer_id) AS customer_count,
    ROUND(AVG(o.order_amount), 2) AS avg_order_amount
FROM customers cu
JOIN first_orders fo ON cu.customer_id = fo.customer_id
JOIN orders o ON cu.customer_id = o.customer_id
GROUP BY CASE WHEN fo.first_order_date::date - cu.signup_date <= 30
              THEN 'fast' ELSE 'slow' END;
"""

Q25 = """
SELECT
    TO_CHAR(cu.signup_date, 'YYYY-MM') AS signup_month,
    TO_CHAR(o.order_date, 'YYYY-MM') AS order_month,
    ((EXTRACT(YEAR FROM o.order_date) - EXTRACT(YEAR FROM cu.signup_date)) * 12) +
    (EXTRACT(MONTH FROM o.order_date) - EXTRACT(MONTH FROM cu.signup_date)) AS months_since_signup,
    COUNT(o.order_id) AS order_count
FROM customers cu
JOIN orders o ON cu.customer_id = o.customer_id
GROUP BY
    TO_CHAR(cu.signup_date, 'YYYY-MM'),
    TO_CHAR(o.order_date, 'YYYY-MM'),
    ((EXTRACT(YEAR FROM o.order_date) - EXTRACT(YEAR FROM cu.signup_date)) * 12) +
    (EXTRACT(MONTH FROM o.order_date) - EXTRACT(MONTH FROM cu.signup_date))
ORDER BY signup_month, months_since_signup;
"""


# ─── Run all queries ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    queries = [
        ("Q1  - Orders with full country name",          Q1),
        ("Q2  - Orders with customer tier",              Q2),
        ("Q3  - Orders with coupon details",             Q3),
        ("Q4  - Orders with country + tier (3 tables)",  Q4),
        ("Q5  - Status history for ORD-1004",            Q5),
        ("Q6  - Countries with order count",             Q6),
        ("Q7  - Customers with no orders",               Q7),
        ("Q8  - All orders with optional coupon info",   Q8),
        ("Q9  - Coupons with usage count",               Q9),
        ("Q10 - Revenue & orders per region",            Q10),
        ("Q11 - Avg order amount per tier",              Q11),
        ("Q12 - Top 5 customers by spending",            Q12),
        ("Q13 - Total discount given per coupon",        Q13),
        ("Q14 - Orders per channel per region",          Q14),
        ("Q15 - Orders outside home country",            Q15),
        ("Q16 - Customers above avg order amount",       Q16),
        ("Q17 - Status change count per order",          Q17),
        ("Q18 - Orders with expired coupons",            Q18),
        ("Q19 - Most popular channel per region",        Q19),
        ("Q20 - Customer value classification",          Q20),
        ("Q21 - Order rank within country",              Q21),
        ("Q22 - Avg hours between status changes",       Q22),
        ("Q23 - Monthly report",                         Q23),
        ("Q24 - Signup speed analysis",                  Q24),
        ("Q25 - Cohort analysis by signup month",        Q25),
    ]

    for label, query in queries:
        run_query(label, query)

    conn.close()
    print("\nDone. Connection closed.")