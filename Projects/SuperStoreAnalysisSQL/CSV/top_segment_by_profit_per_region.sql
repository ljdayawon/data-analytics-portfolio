WITH ProfitPerSegment AS (
  SELECT 
    Region,
    Segment,
    SUM(Profit) AS Total_Profit,
    RANK() OVER (PARTITION BY Region ORDER BY SUM(Profit) DESC) AS rnk
  FROM superstore_dataset_clean.orders
  GROUP BY Region, Segment
)
SELECT Region, Segment, ROUND(Total_Profit,2) AS Total_Profit
FROM ProfitPerSegment
WHERE rnk = 1
ORDER BY Total_Profit DESC;
