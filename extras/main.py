import requests
import pandas as pd
from fun import funcpat


page_url = "http://www.fondear.com/Todo_Charter/Puertos/Cataluna/Cataluna.htm"


r = requests.get(page_url)
df_list = pd.read_html(r.text, flavor='bs4') # this parses all the tables in webpages to a list

starttable = 6 # table num to start from
numtables = 3 # num of tables to read
ntot = starttable + numtables # total df

while starttable < (ntot):
    df = pd.DataFrame(data = df_list[starttable]) # create df from df_list
    df.columns = ['nombre', 'lat', 'lon', 'amarres', 'tel'] # set column names
    df = df.drop([0], axis=0) # drop first row (NaNs)
    df = funcpat(df)

    print(df.head())
    starttable+=1
