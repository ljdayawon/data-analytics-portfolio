SELECT
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(SUM(Profit)/SUM(Sales), 2) AS overall_profit_margin,
    ROUND(SUM(Sales)/COUNT(DISTINCT Order_ID), 2) AS avg_order_value
FROM orders;
