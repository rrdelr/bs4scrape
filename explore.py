import datetime
import json

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from fun import latlonconv, infotoinfo
from ima import imagedl
from placesapi import places_one


def getlinks(list):
    """
    Gets all links from the port directory site
    :param list: The list where the links will be stored
    :return: list with links
    """
    url = 'http://charter.fondear.com/puertos-deportivos-en-espana/'
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'lxml')

    links = [a.get('href') for a in soup.find_all('a', href=True)]


    for link in links:
        if 'Todo_Charter' in link:
            if link not in list:
                list.append(link)

    return list


def getportlinks(url, list):
    """
    Picks through the url and fetches all relevant links
    :param url: the urls where the search will be done
    :param list: the list where the links will be stored
    :return: list with links to individual ports
    """
    part_url = url.split("/")
    safe_url = 'http://www.fondear.com/Todo_Charter/Puertos/' + part_url[5] + '/'
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'lxml')
    links = [a.get('href') for a in soup.find_all('a', href=True)]

    for link in links:
        if 'http' not in link and 'mailto' not in link and 'Todo_Empresa' not in link:
            if link not in list:
                link = safe_url + link
                list.append(link)

    return (list)


def createportdict(url):
    """
    Creates a dict with port data
    :param url: The url with info to be made into a dict
    :return: a dictionary with port info
    """
    part_url = url.split("/")
    region = part_url[5]

    r = requests.get(url)
    df_list = pd.read_html(r.text, flavor='bs4')  # this parses all the tables in webpages to a list
    tbl_desc = pd.DataFrame(data=df_list[1])
    tbl_desc = tbl_desc.replace(np.nan, ".")

    descr = tbl_desc[0][23]
    if descr == "Rampa":
        descr = tbl_desc[0][26]
    elif descr == "Travel lift":
        descr = tbl_desc[0][27]
    elif descr == "Grua":
        descr = tbl_desc[0][28]
    if descr == ".":
        descr = "Descripción no disponible"

    image = imagedl(url)

    try:
        name_tbl = pd.DataFrame(data=df_list[5])
        boat_tbl = pd.DataFrame(data=df_list[6])
        svcs_tbl = pd.DataFrame(data=df_list[7])
        services = {
            "Agua": svcs_tbl.iloc[0][1],
            "Grúa": svcs_tbl.iloc[3][1],
            "Rampa": svcs_tbl.iloc[5][1],
            "Taller": svcs_tbl.iloc[6][1],
            "Muelle de espera": svcs_tbl.iloc[0][3],
            "Bar": svcs_tbl.iloc[1][3],
            "Restaurante": svcs_tbl.iloc[2][3],
            "Supermercado": svcs_tbl.iloc[3][3],
            "Farmacia": svcs_tbl.iloc[1][5],
            "Servicios de primeros auxilios": svcs_tbl.iloc[2][5],
            "Banco": svcs_tbl.iloc[4][5],
            "Alquiler de coches": svcs_tbl.iloc[5][5],
            "Información meteorológica": svcs_tbl.iloc[3][5]
        }
        svcs_items = services.items()
        svcs_list = []
        for key, value in svcs_items:
            if value == 'SI':
                svcs_list.append(key)
        linfo = infotoinfo(name_tbl.iloc[1][0])
        latlonli = latlonconv(name_tbl.iloc[2][0])
        name = name_tbl.iloc[0][0]
        yeezerdict = {
            "port_name": name,
            "region": region,
            # "lat": latlonli[0],
            # "lng": latlonli[1],
            "image_id": image,
            "features": {
                "mooring": ["Número de amarres", str(boat_tbl.iloc[2][1])],
                ###"port_mouth": ["Boca de puerto (mts)", boat_tbl.iloc[2][1]],
                "length": ["Eslora máxima (mts)", str(boat_tbl.iloc[1][1])],
                "draft": ["Calado mínimo (mts)", str(boat_tbl.iloc[0][1])]
            },
            "services": svcs_list,
            "description": descr,
            # "location":linfo[1],
            "email": "n.d.",
            "url": linfo[0],
            "telephone": linfo[2],
            'creation_date': str(datetime.datetime.utcnow()),
            'last_updated': str(datetime.datetime.utcnow()),
            'created_by': 'admin',
            'status': 'up',
            'type': 'anchor'
        }
        return (yeezerdict)
    except:
        try:
            name_tbl = pd.DataFrame(data=df_list[4])
            boat_tbl = pd.DataFrame(data=df_list[5])
            svcs_tbl = pd.DataFrame(data=df_list[6])
            services = {
                "Agua": svcs_tbl.iloc[0][1],
                "Grúa": svcs_tbl.iloc[3][1],
                "Rampa": svcs_tbl.iloc[5][1],
                "Taller": svcs_tbl.iloc[6][1],
                "Muelle de espera": svcs_tbl.iloc[0][3],
                "Bar": svcs_tbl.iloc[1][3],
                "Restaurante": svcs_tbl.iloc[2][3],
                "Supermercado": svcs_tbl.iloc[3][3],
                "Farmacia": svcs_tbl.iloc[1][5],
                "Servicios de primeros auxilios": svcs_tbl.iloc[2][5],
                "Banco": svcs_tbl.iloc[4][5],
                "Alquiler de coches": svcs_tbl.iloc[5][5],
                "Información meteorológica": svcs_tbl.iloc[3][5]
            }
            svcs_items = services.items()
            svcs_list = []
            for key, value in svcs_items:
                if value == 'SI':
                    svcs_list.append(key)
            linfo = infotoinfo(name_tbl.iloc[1][0])
            latlonli = latlonconv(name_tbl.iloc[2][0])
            yeezerdict = {
                "port_name": name,
                "region": region,
                # "lat": latlonli[0],
                # "lng": latlonli[1],
                "image_id": image,
                "features": {
                    "mooring": ["Número de amarres", str(boat_tbl.iloc[2][1])],
                    "length": ["Eslora máxima (mts)", str(boat_tbl.iloc[1][1])],
                    "draft": ["Calado mínimo (mts)", str(boat_tbl.iloc[0][1])]
                },
                "services": svcs_list,
                "description": descr,
                "email": "admin@site.co",
                "url": linfo[0],
                "telephone": linfo[2],
                'creation_date': str(datetime.datetime.utcnow()),
                'last_updated': str(datetime.datetime.utcnow()),
                'created_by': 'admin',
                'status': 'up',
                'type': 'anchor'
            }
            return (yeezerdict)
        except:
            log = "Exception detected. Continuing..."


api = 0
save = 0

list = []
port_list = []
name_list = []

list = getlinks(list)
for url in tqdm(list):
    port_list = getportlinks(url, port_list)
data = []
jobct = len(port_list)
i = 0
for url in tqdm(port_list):
    port = createportdict(url)
    if port is not None:
        try:
            if api:
                port = places_one(port)
            data.append(port)
        except:
            pass

if save:
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
