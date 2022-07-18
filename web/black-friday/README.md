# web/black-friday
## Initial Info
[Watch site](http://host3.metaproblems.com:5900/) provided in the challenge. This site has a drop-down list allowing the end-user to choose the active store being viewed. Inspecting the traffic in the browser or in Burp Suite shows that a cookie called `ww_store` is created which tells the site the current store.
## ww_store
Modifying ww_store and re-requesting the page shows something interesting. Simply adding a single-quote (') will display an error page saying "A DATABASE ERROR HAS OCCURED. PLEASE CONTACT THE ADMINISTRATOR." Perfect! This means there is a SQLI vulnerability! 
Messing around by manually injecting the cookie will provide more details about the vulnerability. Firstly, any quotes or special chars seem to cause the error page, whether or not they are encoded by the browser. So, injection should be done by simply appending further SQL statements after the number for the currently viewed store. Additionally, I could only get boolean blind sqli to work. When a given injected query is true, a blank page with no store will be returned. When a query is false, a page will be returned stating "STORE NOT FOUND."
## SQLMap
Naturally, I attempted to use SQLMap. I tried a variety of parameters and spent a few hours researching problems associated with SQLMap and boolean injection. After I finally achieved the feat of getting the program to recognize the cookie as injectable, it would label it as a false-positive. I have never used this program before (and hadn't really done any sqli) so it was likely user-error, but I gave up and wrote some python code to do the work.
## Python code
I wrote the Python code provided in this directory to solve the challenge. I used the `requests` library, and a lot of messy, trial-and-error code to solve it. First, I wrote a function which would query the store page with a given injected cookie and return true or false based on the response (or notify me on error). 
Next, I tried a variety of ways to discover the other tables in the database, such as INFORMATION_SCHEMA. None of these were sucessful, so I created a list of various names I could think for other tables which would store the promo codes and tested them. I used "AND EXISTS(...)" for the queries.
Success, I found two tables, `stores` and `promos`!
Next I tested various column names which could contain the actual code data, using the same method as above. It ended up being the column named `promo_code`.
Next I brute forced the promo code length using "WHERE LENGTH(promo_code)=...". I found 3 different valid lengths: 6, 8, and 32. I guessed the likely one would be 32, but I tried each of them anyways.
Looping through all possible letters, digits, and some special characters, I brute forced the promo code using "SUBSTRING(...)." As the code progressed I saw "flag" being spelled out. Finally, I got the flag.
```

```
