#Sales & Profit Performance Over Time

SELECT 
	DATE_FORMAT(`Order_Date`, '%Y-%m') AS order_month, # Groups data by month (e.g., '2025-07')
	ROUND((SUM(Sales)),2) AS total_sales,                         # Total sales in each month
	ROUND((SUM(Profit)),2) AS total_profit,                       # Total profit in each month
	ROUND(SUM(Profit)/SUM(Sales), 2) AS profit_margin  # Profitability = Profit / Sales
FROM orders
GROUP BY order_month                                   # Grouping result per month
ORDER BY order_month;                                  # Display results in chronological order
