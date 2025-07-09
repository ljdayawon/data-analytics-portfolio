SELECT 
Sub_Category, 
ROUND((SUM(Sales)), 2) AS Total_Sales, 
ROUND((SUM(Profit)), 2) AS Total_Profit,
ROUND((SUM(Profit)/SUM(Sales)),2) AS Profit_Margin,

CASE
#10% Margin = Industry Heuristic (Rule of Thumb)
	WHEN SUM(Profit)/SUM(Sales) < 0 THEN 'Loss-Making' #Negative
	WHEN SUM(Profit)/SUM(Sales) < 0.1 THEN 'Low Margin' #Less thank 10%
	ELSE 'Healthy' #10% Above
END AS Profit_Status


FROM superstore_dataset_clean.orders

GROUP BY Sub_Category
HAVING SUM(Sales) > 1000
ORDER BY SUM(Sales) DESC;

