from bs4 import BeautifulSoup
import requests

def imagedl(url):
    part_url = url.split("/")
    problems = ["Murcia","Asturias","Cantabria"]
    if part_url[5] in problems:
        safe_url = 'http://www.fondear.com/Todo_Charter/Puertos/' + part_url[5] + '/'
    else:
        safe_url = 'http://www.fondear.com/Todo_Charter/Puertos/' + part_url[5] + '/' + part_url[6] + '/'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    links = soup.find_all('img')
    try:
        ima = links[5]
        imaatts = ima.attrs['src']
        return(safe_url + imaatts)
    except:
        return('NaN')

