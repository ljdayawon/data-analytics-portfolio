SELECT
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(SUM(Profit)/SUM(Sales), 2) AS overall_profit_margin,
FROM orders;
