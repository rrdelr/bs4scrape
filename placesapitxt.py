import requests
import time

api_key = 'AIzaSyCdclKQcQRdBtYm779CPufl1qxPqz6vq88'

placenames = []
dict = []
with open('name_file.txt') as file:
    for line in file:
        line = line.replace("\n", "")
        line = line.replace(' ', '%20')
        placenames.append(line)

print(placenames)

for item in placenames:
    url = "https://maps.googleapis.com/maps/api/place/textsearch/xml?query=puerto%20deportivo%20" + item + "&key=" + api_key
    response = requests.get(url).json()
    time.sleep(1.5)
    dict.append(response)
    print(response)

