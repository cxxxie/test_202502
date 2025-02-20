### What are the top 5 brands by receipts scanned for most recent month?
```sql
WITH most_recent_month AS (
    SELECT DATE_TRUNC('month', MAX(purchase_date)) AS max_month
    FROM receipts
)

SELECT b.brand_name, count(r.receipt_id) AS cnt_receipts
FROM receipts r
INNER JOIN receipt_items ri
ON r.receipt_id = ri.receipt_id
INNER JOIN brands b
ON ri.brand_id = b.brand_id
WHERE DATE_TRUNC('month', r.purchase_date) = (SELECT max_month FROM most_recent_month)
GROUP BY b.brand_name
ORDER BY count(r.receipt_id) DESC
LIMIT 5;
```

### When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
```sql
SELECT rewards_receipt_status, AVG(total_spent) AS avg_spend
FROM receipts
WHERE rewards_receipt_status IN ('Accepted', 'Rejected')
GROUP BY rewards_receipt_status;
```

### Which brand has the most transactions among users who were created within the past 6 months?

```sql
WITH past_six_month_users AS (
    SELECT user_id
    FROM users
    WHERE created_date >= CURRENT_DATE - INTERVAL '6 months'
)

SELECT b.brand_name, COUNT(DISTINCT r.receipt_id) AS cnt_transactions
FROM receipts r
INNER JOIN past_six_month_users p6mu
ON r.user_id = p6mu.user_id
INNER JOIN receipt_items ri
ON r.receipt_id = ri.receipt_id
INNER JOIN brands b
ON ri.brand_id = b.brand_id
GROUP BY b.brand_name
ORDER BY COUNT(DISTINCT r.receipt_id) DESC
LIMIT 1;
```
*All SQL queries above are written using PostgreSQL syntax.