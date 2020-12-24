#!/bin/sh

END=39

rm -f bid.dat
rm -f user.dat
rm -f item.dat
rm -f is_category_of.dat

for index in $(seq 0 $END)
do
	python "parser.py" "ebay_data/items-$index.json"
done

sort -u bid_raw.dat > bid_raw_2.dat
sort -u user_raw.dat > user.dat
sort -u item_raw.dat > item.dat
sort -u is_category_of_raw.dat > is_category_of.dat

i=1
while read name
do
    echo "$i$name" >> bid.dat
    i=$((i=i+1))
done < bid_raw_2.dat

rm -f bid_raw_2.dat

rm -f bid_raw.dat
rm -f user_raw.dat
rm -f item_raw.dat
rm -f is_category_of_raw.dat
