SELECT Customer_Name, SUM(Sales) AS Total_Sales
FROM orders
GROUP BY Customer_Name
ORDER BY Total_Sales DESC
LIMIT 5;

