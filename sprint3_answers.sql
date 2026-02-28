-- Q1: Show all orders with the full country name instead of the country code.
-- Display order_id, order_date, country_name, order_amount.
select order_id,order_date,country_name,order_amount
from orders o
inner join countries c on o.country_code=c.country_code;
-- Q2: Show all orders with the customer's tier.
-- Display order_id, customer_id, tier, order_amount.
select o.order_id,o.customer_id,c.tier,o.order_amount
from orders o
inner join customers c on o.customer_id=c.customer_id;

-- Q3: For orders that used a coupon, show order_id, order_amount, coupon_code, and discount_percent.
select o.order_id,o.order_amount,o.coupon_code,c.discount_percent
from orders o 
inner join coupons c on o.coupon_code=c.coupon_code
where o.coupon_code is not null;
-- Q4: Show all orders with both the country name and the customer tier.
-- Display order_id, country_name, tier, order_amount. (3 table join)
select o.order_id,coun.country_name,cu.tier,o.order_amount 
from orders o
inner join countries coun on o.country_code=coun.country_code
inner join customers cu on o.customer_id=cu.customer_id;
-- Q5: Show the full status history for order ORD-1004.
-- Display order_id, status, changed_at, ordered by time.
select order_id,status,changed_at
from order_status_history
where order_id='ORD-1004'
order by changed_at;
-- Q6: List all countries with their total number of orders. Include countries with 0 orders.
-- Display country_name, order_count.
select c.country_name,o.order_amount 
from countries c 
left join orders o on o.country_code=c.country_code;
-- Q7: Find all customers who have never placed an order.
-- Show customer_id, home_country, tier, signup_date.
select c.customer_id,c.home_country,c.tier,c.signup_date
from customers c 
left join orders o on c.customer_id=o.customer_id
where o.customer_id is null;
-- Q8: Show all orders, and for those that used a coupon, show the discount details.
-- Orders without a coupon should still appear with NULL discount info.
-- Display order_id, order_amount, coupon_code, discount_percent.
select o.order_id,o.order_amount,c.coupon_code,c.discount_percent
from orders o 
left join coupons c on o.coupon_code=c.coupon_code;
-- Q9: List all coupons and show how many times each was used.
-- Include coupons that were never used (should show 0).
-- Display coupon_code, is_active, times_used.
select c.coupon_code,c.is_active,count(o.coupon_code) as times_used
from coupons c
left join orders o on o.coupon_code = c.coupon_code
group by c.coupon_code, c.is_active
order by times_used;
-- Q10: For each region, calculate the total revenue and number of orders.
-- Display region, total_revenue, order_count. Order by revenue descending.
select c.region,sum(o.order_amount) as total_revenue,count(o.order_id) as order_count
from orders o 
inner join countries c on o.country_code=c.country_code
group by c.region
order by total_revenue DESC;
-- Q11: For each customer tier, calculate the average order amount and total number of orders.
-- Display tier, order_count.
select c.tier,round(avg(o.order_amount),2) as order_count
from orders o
inner join customers c on c.customer_id=o.customer_id
group by c.tier;

-- Q12: Find the top 5 customers by total spending.
-- Show customer_id, tier, home_country (as full country name), total_spent.
-- Order by total descending.
select o.customer_id,c.tier,coun.country_name,sum(o.order_amount) as total_spending
from customers c 
inner join countries coun on coun.country_code=c.home_country
inner join orders o on o.customer_id=c.customer_id
group by o.customer_id,c.tier,coun.country_name
order by total_spending desc
limit 5;
-- Q13: For each coupon, calculate the total discount amount given away (order_amount × discount_percent / 100).
-- Show coupon_code, times_used, total_discount_given.
select c.coupon_code, count(o.coupon_code) as times_used, round(sum(o.order_amount * c.discount_percent/100),2) as total_discount_given
from coupons c
inner join orders o on o.coupon_code=c.coupon_code
group by c.coupon_code;
-- Q14: Show the number of orders per channel per region.
-- Display region, channel, order_count. Only include channels that aren't NULL.
select o.channel,c.region,count(o.order_id) as order_count 
from countries c 
inner join orders o on o.country_code=c.country_code
where o.channel is not null
group by o.channel,c.region;
-- Q15: Find all orders where the customer is ordering from a different country than their home_country.
-- Show order_id, customer_id, home_country, order_country, order_amount.
select o.order_id,o.customer_id,c.home_country,o.country_code as order_country,o.order_amount
from orders o 
inner join customers c on c.customer_id=o.customer_id
where o.country_code != c.home_country;

-- Q16: Find customers whose average order amount is higher than the overall average.
-- Show customer_id, tier, avg_amount, overall_avg.
select c.customer_id,c.tier,round(avg(o.order_amount),2) as avg_amount
from customers c 
inner join orders o on o.customer_id=c.customer_id
group by c.customer_id,c.tier
having avg(o.order_amount) > (select round(avg(order_amount),2) from orders);

-- Q17: For each order, find how many status changes it went through.
-- Show order_id, order_amount, num_status_changes. Order by changes descending.
select o1.order_id,o1.order_amount, count(o2.changed_at) as num_status_changes
from orders o1 
inner join order_status_history o2 on o2.order_id=o1.order_id
group by o1.order_id,o1.order_amount
order by num_status_changes desc;

-- Q18: Find all orders that used a coupon that was expired at the time of the order (order_date > valid_until).
-- Show order_id, order_date, coupon_code, valid_until.
select o.order_id,o.order_date,c.coupon_code,c.valid_until
from orders o 
inner join coupons c on c.coupon_code=o.coupon_code
where o.order_date > c.valid_until;

-- Q19: Find the most popular channel in each region.
-- Show region, channel, order_count.


-- Q20: Using a CTE, calculate each customer's total spending, then classify them as
-- 'high_value' (> 1000), 'medium_value' (500–1000), or 'low_value' (< 500).
-- Show customer_id, tier, total_spent, value_class.
with customer_spending as (
select c.customer_id,c.tier,round(sum(o.order_amount),2) as total_spent,
case 
  when round(sum(o.order_amount),2)>1000 then 'high_value'
  when round(sum(o.order_amount),2) between 500 and 1000 then 'medium_value'
  else 'low_value' 
end as value_class
from customers c
inner join orders o on o.customer_id=c.customer_id
group by c.customer_id,c.tier
)
select * from customer_spending;

-- Q21: For each order, show its rank within its country by order amount (highest first).
-- Also show the country's total order count.
-- Display order_id, country_name, order_amount, country_rank, country_total_orders.
select o.order_id,c.country_name,o.order_amount,
rank() over(partition by c.country_name order by o.order_amount desc) as country_rank,
count(o.order_id) over(partition by c.country_name) as country_total_orders
from orders o
inner join countries c on o.country_code=c.country_code;


-- Q22: Calculate the average time between status changes for each order (in hours).
-- Show order_id, num_changes, avg_hours_between_changes.
-- Only include orders with at least 2 status changes.


-- Q23: Write a query that produces a monthly report showing:
-- month, total_orders, total_revenue, unique_customers,
-- coupon_based_orders, avg_order_amount, revenue from first-time vs returning customers.


-- Q24: Find customers who placed their first order within 30 days of signing up vs those who took longer.
-- Show signup_speed ('fast' or 'slow'), customer_count, avg_order_amount.


-- Q25: Create a cohort analysis: group customers by signup month, then for each cohort
-- show how many orders they placed in each subsequent month.
-- Display signup_month, order_month, months_since_signup, order_count.