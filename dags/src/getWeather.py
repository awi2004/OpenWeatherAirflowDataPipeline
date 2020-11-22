import requests
import os
import sys
import pickle


def get_weather(cities):
    """
    Query openweathermap.com's API and to get the weather for
    different cities and then dump the list of json to the //data/ directory
    with the file name "weather.obj"
    """
    # list to store json
    json_list_weather = []
    for i in range(0, len(cities)):

        # paramaters = {'q': 'Berlin, DE', 'appid': '25237a5210330ad588a2a33c388da468'}
        paramaters = {'q': cities[i], 'appid': '25237a5210330ad588a2a33c388da468'}

        result = requests.get("http://api.openweathermap.org/data/2.5/weather?", paramaters)

        # If the API call was sucessful, get the json and dump it to a file with
        # today's date as the title.
        if result.status_code == 200:
            # Get the json data
            json_data = result.json()
            json_list_weather.append(json_data)

        else:
            print("Error In API call.")

    pickle_dir_name = os.path.join(os.path.dirname(__file__), 'data', 'weather.obj')
    pickle.dump(json_list_weather, open(pickle_dir_name, 'wb'))
    data = pickle.load(open(pickle_dir_name, 'rb'))


if __name__ == "__main__":
    get_weather(sys.argv[1:])
