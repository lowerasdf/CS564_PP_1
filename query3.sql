WITH CountCategory as (SELECT ItemID, COUNT(*) as Count 
FROM IsCategoryOf
GROUP BY ItemID)
SELECT COUNT(*)
From CountCategory 
WHERE Count == 4;