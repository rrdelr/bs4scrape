import json
import os
import unicodedata
import time

from google_images_download import google_images_download  # importing the library


response = google_images_download.googleimagesdownload()  # class instantiation


def googleimagedown(word):
    imagedir = word
    arguments = {"keywords": word, "limit": 3, "print_urls": False, "image_directory": imagedir,
                 "prefix_keywords": "Puerto Deportivo", "suffix_keywords": "Espana",
                 "output_directory": "downloads", "format": "jpg", "verbose": False}  # creating list of arguments
    paths = response.download(arguments)  # passing the arguments to the function
    time.sleep(3)
    print(paths)
    return paths[0]["Puerto Deportivo " + word + " Espana"]


def downloadimages(filedata):
    data = []
    os.mkdir("assets")
    numdir = 0

    for port in filedata:
        portname = port["port_name"]
        portname = unicodedata.normalize('NFKD', portname).encode('ascii', 'ignore')
        portname = str(portname)
        portname = portname.replace("b'", "")
        portname = portname.replace("'", "")

        pndir = portname.replace(" ", "_")
        try:
            os.mkdir("assets\\{0}".format(pndir))
        except:
            pndir = "{0}_{1}".format(pndir, numdir)
            os.mkdir("assets\\{0}".format(pndir))
            numdir += 1
        list = googleimagedown(portname)
        listch = []
        n = 100
        for url in list:
            url = url.replace("C:\\Users\\RRX\\PycharmProjects\\NORAY\\bs4scrap\\", "")  # replace abs path with rel
            os.rename(url, "assets\\{0}\\{1}.jpg".format(pndir, n))  # rename file
            url = "assets\\{0}\\{1}.jpg".format(pndir, n)  # fix reference to file in listch
            n += 1
            listch.append(url)
        port["image_id"] = listch
        print(listch)
        data.append(port)

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
