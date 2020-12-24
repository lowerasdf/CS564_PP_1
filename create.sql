drop table if exists BID;
drop table if exists USER;
drop table if exists ITEM;
drop table if exists IsCategoryOf;



create table BID (
	BidID 		integer primary key,
	Amount		real,
	Time		varchar(50),
	SellerID	varchar(50) not null,
	BidderID	varchar(50),
	ItemID		integer not null,
	foreign key (SellerID) references USER, 
	foreign key (BidderID) references USER, 
	foreign key (ItemID) references ITEM
);

create table USER (
	UserID 	varchar(50) primary key not null,
	Rating		integer not null,
	Location	varchar(50),
	Country	varchar(50)
);

create table ITEM (
	ItemID 	integer not null,
	Name		varchar(50) not null,
	Description	varchar(500),
	Buy_Price	real,
    First_Bid	real not null,
	Started	varchar(50) not null,
    Ends		varchar(50) not null,
    Currently	real not null,
	Number_of_Bids	integer not null,
    primary key (ItemID)
);

create table IsCategoryOf (
	ItemID 		integer not null,
	CategoryName		varchar(50) not null,
	primary key (ItemID, CategoryName),
	foreign key (ItemID) references ITEM
);
