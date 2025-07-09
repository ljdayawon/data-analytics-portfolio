#Customer Segmentation & Behavior
SELECT 
	`Customer_ID`, 
	`Customer_Name`,
	Segment,
	COUNT(DISTINCT `Order_ID`) AS order_count,   		    #How many separate orders each customer made
	ROUND((SUM(Sales)),2) AS total_sales,               #How much they bought (revenue)
	ROUND((SUM(Profit)),2) AS total_profit              #How much profit they brought in
FROM orders
GROUP BY `Customer_ID`, `Customer_Name`, Segment 		#Group by each customer + their segment
ORDER BY total_sales DESC                      			#Show top customers by sales
LIMIT 10;                                      			#Only show the top 10
