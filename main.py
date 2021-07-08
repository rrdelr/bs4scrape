import time
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from functions import latlonconv, infotoinfo, svcslist, yzrdict
from placesapi import places_one
from imagesdownload import downloadimages


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

        svcs_list = svcslist(svcs_tbl)
        linfo = infotoinfo(name_tbl.iloc[1][0])
        latlonli = latlonconv(name_tbl.iloc[2][0])
        name = name_tbl.iloc[0][0]
        return (yzrdict(name, region, image, boat_tbl, svcs_list, descr, linfo))
    except:
        try:
            name_tbl = pd.DataFrame(data=df_list[4])
            boat_tbl = pd.DataFrame(data=df_list[5])
            svcs_tbl = pd.DataFrame(data=df_list[6])

            svcs_list = svcslist(svcs_tbl)
            linfo = infotoinfo(name_tbl.iloc[1][0])
            latlonli = latlonconv(name_tbl.iloc[2][0])
            name = name_tbl.iloc[0][0]
            return (yzrdict(name, region, image, boat_tbl, svcs_list, descr, linfo))
        except:
            log = "Exception detected. Continuing..."


### MAIN BLOCK ###


api = 0 # Hacer uso de API de Google Maps

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
    time.sleep(1)
    port = createportdict(url)
    if port is not None:
        try:
            if api:
                port = places_one(port)
            data.append(port)
        except:
            pass

downloadimages(data)
