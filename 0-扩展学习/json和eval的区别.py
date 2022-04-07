import json

sss = '{"member_id":round(float(202+1),2),"title":null,"amount":2000,"loan_rate":12.0,"loan_term":3,"loan_date_type":1,"bidding_days":5}'

if sss.find("null") != -1:
    sss = sss.replace("null", "None")

# s = json.loads(sss)
s = eval(sss)
print(s)
