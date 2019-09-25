
# coding: utf-8



import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
from sendemailOutlook import sendmail
from time import sleep
from decimal import Decimal
import datetime
from dateutil import relativedelta

url="url"

username= 'username'
password='password'

#Ids for the 36 states and the FCT
state_ids=['FHlOerryBjk','OgjFloqKoqk','qLiKWoddwFu','ziJ3yxfgb3m','MXrZyuS9E7A','RLySnRCE1Gy','ns3vF75Y0bF','caG44DzHu6F','m0rZG06GdPe',
 'xWSEoKmrbBW','aMQcvAoEFh0','iilma7EajGc','Quac4RHRtaZ','HYCMnXqLDPV','bSfaEpPFa9Y','FmOhtDnhdwU','MJVVi73YayJ','tjLatcokcel',
 'M689V9w3Gs3','cTIw3RXOLCQ','S7Vs7ifJKlh','uKlacgs9ykR','jReUW6NCPkL','H2ZhSMudlMI','gzLOszDWdqM','RYEnw3sMDyE','fBInDsbaQHO',
 'r3IK5qdHsZ6','hfNPq5F4mjr','yx3QJHm86vW','TFY8aaVkCtV','BmWTbiMgEai','Gq37IyyjUfj','jXngIDniC8t','Ym1fEhWFWYI','FmH4buccgqx','Nko8QFDmYmq']

def make_query(ou,indicator,pe):    
    headers = {
        'Accept': 'application/json',
    }

    params = (
        ('dimension', 'ou:%s'%ou),
        ('filter', 'dx:%s'%indicator),
        ('filter', 'pe:%s'%pe),

    )
    s = requests.Session()
    response = s.get(url + "api/26/analytics", headers=headers, params=params, auth=(username, password))

    if response.ok:
        print(" %d Connection Granted " %response.status_code )
    response.headers['content-type']
    query=response.json()
    return query

def build_query(states,indicator,period):
    count=0
    query_list=[]
    for state in states:
        query=make_query(state,indicator,period)
        try:
            query_essentail=[query['metaData']['items'][state]['name'],query['rows'][-1][1]]
            query_list.append(query_essentail)
            if not query_list:
                return "No Data for %s"%period
            indicator_name=query['metaData']['items'][indicator]['name']
            period_str=query['metaData']['items'][period]['name']
        except:
            pass
    return query_list,indicator_name,period_str


def trigger_notification(indicators_and_thresholds,email_receivers,period='201501'):
    """
    inputs: 
    indicators_and_thresholds=Dict of indicators and corresponding threshold 
    email_receivers=dict of name and dict of email receivers
    outputs:
    Email Status
    Number of outliers discovered
    """
    indicators=list(indicators_and_thresholds.keys())
    period=period
    for indicator in indicators:
        query_list,indicator_name,period_str=build_query(state_ids,indicator,period)
        query_df=pd.DataFrame(query_list, columns=['State','Value'])

        query_df['Value']=pd.to_numeric(query_df['Value'], errors= 'coerce',downcast='float') #Converts value column from numerical str to float else to NAN 
        query_df_clean=query_df.dropna().reset_index(drop=True) #drop all rows with nan and reset index accordingly
        print(query_df_clean)
        value_l=dict(zip(list(query_df_clean.State),list(query_df_clean.Value)))
        if not value_l:
            return "No Updated data value for %s in the month %s" %(indicator,period)

        threshold= indicators_and_thresholds[indicator] # Threshold 
        count=0
        for state,value in value_l.items():
            if value> threshold:
                count+=1
                value=round(Decimal(value),2) #Round up value to 2 decimal places 
                state=state.split(' ', 1)[1] #Splits state using space into 2 items only , the first and the rest, and the rest is taken.
                sendmail(email_receivers,indicator=indicator_name,orgUnit=state,value=value,period=period_str)
                print("    Above the set threshold for %s in the month %s at %s " %(indicator_name,period_str,state) )

        print()
        print("In Total, %d outlier(s) discovered for %s in the month %s  " %(count,indicator_name,period_str) )
        
    return "Check Completed"


#CHOOSING THE THRESHOLD FROM THE OUTLIER
def threshold_stat(data):
    import numpy as np
    #data=list(dataval_df_clean.value)

    # calculate interquartile range
    q25, q75 = np.percentile(data, 25), np.percentile(data, 75)
    iqr = q75 - q25
    cut_off = iqr * 1.5
    lower, upper = q25 - cut_off, q75 + cut_off
    # identify outliers
    outliers = [x for x in data if x > upper]
    if not outliers:
        return "No Upper Outliers"
    maxi=int(max(outliers)) #Get the max of upper outlier
    thres= round(maxi,-1) #Round up to the nearest tens
    threshold= lambda x,y: x-10 if x > y else x
    return threshold(thres,maxi)


# ### Only the indicators_and_thresholds and  the email_receivers dictionaries below need to be updated and changed to trigger notification for different users and for different indicators with their corresponding threshold for all the states.

# In[28]:




indicators_and_thresholds={'HH0iQLlqddM':7000.0}
email_receivers={'Francis':'email@gmail.com','Henry':'email@gmail.com','Abdul':'email@gmail.com'}




def production():
    target = datetime.date(2019,10,14)
    tomorrow=24*60*60
    today=datetime.date.today()

    while True:
        if target == today:
            pad_zero=lambda x: '0'+str(x) if len(str(x)) == 1 else str(x)
            period=str(today.year)+ pad_zero(today.month-1)
            if today.month == 1 :
                period=str(today.year-1)+ '12'
            trigger_notification(indicators_and_thresholds,email_receivers,period=period)
            target=today + relativedelta.relativedelta(months=1) #Target becomes same day next month

        sleep(tomorrow)
        today=datetime.date.today()

def test():
    target = datetime.datetime(2019,9,19,4,20,0)
    tomorrow=5*60
    today = datetime.datetime.now()
    period='201909'

    while True:
        if target <= today:
            trigger_notification(indicators_and_thresholds,email_receivers,period=period)
            target=today + relativedelta.relativedelta(minutes=15) 

        sleep(tomorrow)
        today = datetime.datetime.now()




if __name__ == '__main__':
    test()

