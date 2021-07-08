import pandas as pd
import requests
import json

api_key = 'AIzaSyCdclKQcQRdBtYm779CPufl1qxPqz6vq88'

address_list = list(McDonalds_data['address']) #prepare variable to pass to URL
state_list = list(McDonalds_data['state']) #prepare variable to pass to URL
placesAPI_data = pd.DataFrame(columns=['formatted_address', 'name', 'permanently_closed']) #initialize dataframe
for i in range(len(address_list)):
    address = address_list[i].replace(' ', '%20') #make sure there are no blank spaces for the URL
    state = state_list[i]
    address_search = "McDonald's%20"+ address + ",%20" + state + ",%20USA"
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+ address_search + \
        "&inputtype=textquery&fields=name,formatted_address,permanently_closed&key="+ api_key
    response = requests.get(url).json()
    placesAPI_data = pd.concat([placesAPI_data, pd.DataFrame(response['candidates'])], ignore_index=True, sort=False) #append retrieved information to a dataframe
    time.sleep(1.25)
    print(i, " " , address_search) #print for visual control