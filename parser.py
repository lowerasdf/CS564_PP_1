
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        bid_data = []
        user_data = []
        item_data = []
        is_category_of_data = []
        for item in items:
            item["Name"] = "\"" + "\"\"".join(item["Name"].strip().split('\"')) + "\""
            if "Location" in item.keys():
                item["Location"] = "\"" + "\"\"".join(item["Location"].strip().split('\"')) + "\""
                #item["Location"] = "\"" + item["Location"].strip() + "\""
            else:
                item["Location"] = "\"" + "NULL" + "\""
            if "Country" in item.keys():
                item["Country"] = "\"" + "\"\"".join(item["Country"].strip().split('\"')) + "\""
                #item["Country"] = "\"" + item["Country"].strip() + "\""
            else:
                item["Country"] = "\"" + "NULL" + "\""
            item["Seller"]["UserID"] = "\"" + item["Seller"]["UserID"].strip() + "\""
            
            item["Currently"] = transformDollar(item["Currently"])
            item["First_Bid"] = transformDollar(item["First_Bid"])
            item["Started"] = "\"" + transformDttm(item["Started"]) + "\""
            item["Ends"] = "\"" + transformDttm(item["Ends"]) + "\""
            
            if "Buy_Price" not in item.keys():
                item["Buy_Price"] = -1
            
            if isinstance(item["Description"], str):
                item["Description"] = "\"" + "\"\"".join(item["Description"].strip().split('\"')) + "\""
            else:
                item["Description"] = "NULL"
            
            for category in item["Category"]:
                category = category.strip()
                is_category_of_data_entry = {
                    "ItemID" : item["ItemID"],
                    "CategoryName" : category
                }
                is_category_of_data.append(is_category_of_data_entry)
                
            if item["Bids"] is not None:
                for bid in item["Bids"]:
                    bid["Bid"]["Bidder"]["UserID"] = "\"" + bid["Bid"]["Bidder"]["UserID"].strip() + "\""
                    if "Location" in bid["Bid"]["Bidder"].keys():
                        bid["Bid"]["Bidder"]["Location"] = "\"" + "\"\"".join(bid["Bid"]["Bidder"]["Location"].strip().split('\"')) + "\""
                        #bid["Bid"]["Bidder"]["Location"] = "\"" + bid["Bid"]["Bidder"]["Location"].strip() + "\""
                    else:
                        bid["Bid"]["Bidder"]["Location"] = "\"" + "NULL" + "\""
                    if "Country" in bid["Bid"]["Bidder"].keys():
                        bid["Bid"]["Bidder"]["Country"] = "\"" + "\"\"".join(bid["Bid"]["Bidder"]["Country"].strip().split('\"')) + "\""
                        #bid["Bid"]["Bidder"]["Country"] = "\"" + bid["Bid"]["Bidder"]["Country"].strip() + "\""
                    else:
                        bid["Bid"]["Bidder"]["Country"] = "\"" + "NULL" + "\""
                    bid["Bid"]["Time"] = "\"" + transformDttm(bid["Bid"]["Time"]) + "\""
                    bid["Bid"]["Amount"] = transformDollar(bid["Bid"]["Amount"])
                    
                    bid_data_entry = {
                        "BidID" : "",
                        "Amount" : bid["Bid"]["Amount"],
                        "Time" : bid["Bid"]["Time"],
                        "SellerID" : item["Seller"]["UserID"],
                        "BidderID" : bid["Bid"]["Bidder"]["UserID"],
                        "ItemID" : item["ItemID"]
                    }
                    bid_data.append(bid_data_entry)
                    
                    user_data_entry = {
                        "UserID": bid["Bid"]["Bidder"]["UserID"],
                        "Rating": bid["Bid"]["Bidder"]["Rating"],
                        "Location" : bid["Bid"]["Bidder"]["Location"],
                        "Country" : bid["Bid"]["Bidder"]["Country"]
                    }
                    user_data.append(user_data_entry)
            else:
                bid_data_entry = {
                    "BidID" : "",
                    "Amount" : -1,
                    "Time" : "\"" + "NULL" + "\"",
                    "SellerID" : item["Seller"]["UserID"],
                    "BidderID" : "\"" + "NULL" + "\"",
                    "ItemID" : item["ItemID"]
                }
                bid_data.append(bid_data_entry)
            
            user_data_entry = {
                "UserID" : item["Seller"]["UserID"],
                "Rating" : item["Seller"]["Rating"],
                "Location" : item["Location"],
                "Country" : item["Country"]
            }
            user_data.append(user_data_entry)
            
            item_data_entry = {
                "ItemID" : item["ItemID"],
                "Name" : item["Name"],
                "Description" : item["Description"],
                "Buy_Price" : item["Buy_Price"],
                "First_Bid" : item["First_Bid"],
                "Started" : item["Started"],
                "Ends" : item["Ends"],
                "Currently" : item["Currently"],
                "Number_of_Bids" : item["Number_of_Bids"]
            }
            item_data.append(item_data_entry)
            
        with open("bid_raw.dat", "a") as f:
            for bid in bid_data:
                line = ""
                for _, val in bid.items():
                    line += str(val) + "|"
                f.write(line[:-1] + "\n")
        
        with open("user_raw.dat", "a") as f:
            for user in user_data:
                line = ""
                for _, val in user.items():
                    line += str(val) + "|"
                f.write(line[:-1] + "\n")
        
        with open("item_raw.dat", "a") as f:
            for item in item_data:
                line = ""
                for _, val in item.items():
                    line += str(val) + "|"
                f.write(line[:-1] + "\n")
        
        with open("is_category_of_raw.dat", "a") as f:
            for item in is_category_of_data:
                line = ""
                for _, val in item.items():
                    line += str(val) + "|"
                f.write(line[:-1] + "\n")

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)

string = "te\"s\"t"
f"\"{string}\""

"\"\"".join(string.split('\"'))

string.split("e")


