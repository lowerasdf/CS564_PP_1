WITH Max as 
    (SELECT ItemID, MAX(Currently) 
    FROM ITEM)
SELECT ItemID 
FROM max