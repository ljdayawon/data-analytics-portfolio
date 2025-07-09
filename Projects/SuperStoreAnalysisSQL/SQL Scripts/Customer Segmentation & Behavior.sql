SELECT 
  `Customer ID`, 
  `Customer Name`,
  Segment,
  COUNT(DISTINCT `Order ID`) AS order_count,   # How many separate orders each customer made
  SUM(Sales) AS total_sales,                   # How much they bought (revenue)
  SUM(Profit) AS total_profit                  # How much profit they brought in
FROM orders
GROUP BY `Customer ID`, `Customer Name`, Segment # Group by each customer + their segment
ORDER BY total_sales DESC                      # Show top customers by sales
