#Sub-Category Sales and Profitability Analysis

SELECT 
	Category,
	`Sub_Category`,
	ROUND((SUM(Sales)),2) AS total_sales,                   #Total sales per product
	ROUND((SUM(Profit)),2) AS total_profit,                 #Total profit per product
	ROUND(SUM(Profit)/SUM(Sales), 2) AS profit_margin 		#How profitable the product is
FROM orders
GROUP BY Category, `Sub_Category`							#Grouping at the product level
ORDER BY total_profit ASC;                         			#Show least profitable products first
