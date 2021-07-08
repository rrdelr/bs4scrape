import requests
import time
import warnings

warnings.filterwarnings("ignore")

api_key = '' ##### API KEY

def places(data):
    for x in data:
        # Data prep
        xlname = x["port_name"]
        xlname = xlname.replace("\n", "")
        xlname = xlname.replace(' ', '%20')
        print(xlname)
        # API Call
        x["xlname"] = xlname
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=puerto%20deportivo%20" + xlname + \
              "%20" + x["region"] + "%20Spain&key=" + api_key
        response = requests.get(url,verify=False).json()
        #print(response)
        #print(response["results"][0]["geometry"]["location"]["lat"])

        # Final values
        x["location"] = response["results"][0]["formatted_address"]
        x["score"] = response["results"][0]["rating"]
        x["lat"] = response["results"][0]["geometry"]["location"]["lat"]
        x["lng"] = response["results"][0]["geometry"]["location"]["lng"]
        # print(x)
        time.sleep(0.1)

def places_one(x):
    # Data prep
    xlname = x["port_name"]
    xlname = xlname.replace("\n", "")
    xlname = xlname.replace(' ', '%20')
    # API Call
    x["xlname"] = xlname
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=puerto%20deportivo%20" + xlname + \
          "%20" + x["region"] + "%20spain"+ "&key=" + api_key
    response = requests.get(url, verify=False).json()
    # print(response)
    # print(response["results"][0]["geometry"]["location"]["lat"])

    # Final values
    x["location"] = response["results"][0]["formatted_address"]
    try:
        x["score"] = response["results"][0]["rating"]
    except:
        x["score"] = 0
    x["lat"] = response["results"][0]["geometry"]["location"]["lat"]
    x["lng"] = response["results"][0]["geometry"]["location"]["lng"]
    # print(x)
    time.sleep(1)
    return x


    # Old unimplemented
    # for item in placenames:
    #     url = "https://maps.googleapis.com/maps/api/place/textsearch/xml?query=puerto%20deportivo%20" + item +"&key=" + api_key
    #     response = requests.get(url).json()
    #     time.sleep(1.5)
    #     dict.append(response)
    #     print(response)

# Test run
# datatest = [{"port_name":"Port Royale"}]
# places(datatest)