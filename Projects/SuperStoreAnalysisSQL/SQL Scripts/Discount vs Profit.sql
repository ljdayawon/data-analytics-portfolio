#Discount vs Profit

SELECT 
	ROUND(Discount, 2) AS discount_rate,    	#Group discounts (e.g., 0.1, 0.2, etc.)
	COUNT(*) AS transactions,              		#Number of sales with that discount
	ROUND((AVG(Sales)),2) AS avg_sales,         #Avg. sale value at that discount rate
	ROUND((AVG(Profit)),2) AS avg_profit        #Avg. profit at that discount rate
FROM superstoredb.orders
GROUP BY discount_rate                  		#Analyze by each discount level
ORDER BY discount_rate;
