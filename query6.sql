SELECT COUNT (DISTINCT SellerID)
FROM BID 
WHERE SellerID in (SELECT BidderID ID FROM BID)
