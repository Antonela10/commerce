# Commerce

## Commerce project description:

This project started as a part of CS50's Web Programming with Python and JavaScript and their problem set task. 
It is an eBay-like e-commerce auction site where users can post auction listings, place bids on listings, comment on those listings, and add listings to their “watchlist”.

Before users create their profiles and log in, they can see all the *Active Listings* as well as product *Categories*.
In addition to that, on the *navbar* they have links where they can *Register* their profile if they don't have it and a link to *Log In* if they are not logged.

![alt text](images/Front_page_not_logged_in_1.png)


After they're logged in, additional links appear in the navbar: *Watchlist*, *Create Listing*, *Closed Listings* and *Log Out*:

![alt text](images/Front_page_logged_in_1.png)

Users can create their own listings:

![alt text](images/Create_listing_1.png)

If the user is not the one that created a particular listing, user can add it to its watchlist as well as place bids:

![alt text](images/Product_page_1.png)

Once the product has been added to the watchlist, user can see all the products on its watchlist, and it can also remove them from the watchlist:

![alt text](images/User_watchlist_1.png)

User can also remove the product from the watchlist from the product's page as well:

![alt text](images/Product_page_2.png)

If we try to place a bid that is smaller than the current product price, we get a message that our bid is not big enough:

![alt text](images/Product_page_bid_1.png)
![alt text](images/Product_page_bid_2.png)

if we place a bid that is bigger, that bid also becomes the product's current price:

![alt text](images/Product_page_bid_3.png)


