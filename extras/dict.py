import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

url = "C:/Users/RRX/Downloads/xml.xml"

page_sourced = requests.get(url).content #add .content here
html_content = BeautifulSoup(page_sourced, "html.parser")
r = requests.get(url)
df_list = pd.read_html(r.text, flavor='bs4') # this parses all the tables in webpages to a list

region_tbl = pd.DataFrame(data=df_list[1])
name_tbl = pd.DataFrame(data=df_list[5])
boat_tbl = pd.DataFrame(data=df_list[6])
svcs_tbl = pd.DataFrame(data=df_list[7])

tbl_desc = pd.DataFrame(data=df_list[1])
tbl_desc = tbl_desc.replace(np.nan, ".")
descr = tbl_desc[0][26]
if descr == ".":
    descr = "n.d."


sitedict = {
    "nombre":name_tbl.iloc[0][0],
    "info":name_tbl.iloc[1][0],
    "loc (TBF)":name_tbl.iloc[2][0],
    "region":region_tbl.iloc[3][0],
    "calado":boat_tbl.iloc[0][1],
    "eslora":boat_tbl.iloc[1][1],
    "amarres":boat_tbl.iloc[2][1],
    "agua":svcs_tbl.iloc[0][1],
    "grua":svcs_tbl.iloc[3][1],
    "rampa":svcs_tbl.iloc[5][1],
    "taller":svcs_tbl.iloc[6][1],
    "muelle epera":svcs_tbl.iloc[0][3],
    "bar":svcs_tbl.iloc[1][3],
    "restaurante":svcs_tbl.iloc[2][3],
    "supermercado":svcs_tbl.iloc[3][3],
    "farmacia":svcs_tbl.iloc[1][5],
    "primeros auxilios":svcs_tbl.iloc[2][5],
    "banco":svcs_tbl.iloc[4][5],
    "alquiler coches":svcs_tbl.iloc[5][5],
    "info meteo":svcs_tbl.iloc[3][5],
    "descripcion":descr
}

#print(sitedict)
#print(name_tbl.iloc[1][0])
splitst = name_tbl.iloc[1][0].split()
siteb = "n.A."
for x in splitst:
    if "www" in x:
        siteb = x
        #print(siteb)
    if not list:
        siteb = "n.A."

splitstb = name_tbl.iloc[1][0].split("Telf:")
if siteb:
    splitstb[1] = splitstb[1].strip(siteb)
#print(splitstb)

# sitedict = {
#     "nombre": name_tbl.iloc[0][0],
#     "info": name_tbl.iloc[1][0],
#     "loc (TBF)": name_tbl.iloc[2][0],
#     "region": region_tbl.iloc[3][0],
#     "calado": boat_tbl.iloc[0][1],
#     "eslora": boat_tbl.iloc[1][1],
#     "amarres": boat_tbl.iloc[2][1],
# }
# services = {
#     "Agua": svcs_tbl.iloc[0][1],
#     "Grúa": svcs_tbl.iloc[3][1],
#     "Rampa": svcs_tbl.iloc[5][1],
#     "Taller": svcs_tbl.iloc[6][1],
#     "Muelle de espera": svcs_tbl.iloc[0][3],
#     "Bar": svcs_tbl.iloc[1][3],
#     "Restaurante": svcs_tbl.iloc[2][3],
#     "Supermercado": svcs_tbl.iloc[3][3],
#     "Farmacia": svcs_tbl.iloc[1][5],
#     "Servicios de primeros auxilios": svcs_tbl.iloc[2][5],
#     "Banco": svcs_tbl.iloc[4][5],
#     "Alquiler de coches": svcs_tbl.iloc[5][5],
#     "Información meteorológica": svcs_tbl.iloc[3][5]
# }