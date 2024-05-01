import requests
import json

def geolocate(ip):
    response = requests.get(f'http://ipinfo.io/{ip}/json')

    return json.loads(response.text)

def display_geolocation(result):
    string = []

    if 'country' in result:
        string.append('    ' + '\033[1;37mCountry\033[0m'.ljust(25, ' ') + result['country'])

    if 'region' in result:
        string.append('    ' + '\033[1;37mRegion\033[0m'.ljust(25, ' ') + result['region'])

    if 'city' in result:
        string.append('    ' + '\033[1;37mCity\033[0m'.ljust(25, ' ') + result['city'])

    if 'postal' in result:
        string.append('    ' + '\033[1;37mPostal\033[0m'.ljust(25) + result['postal'])

    if len(string) > 0:
        print('\n'.join(string))

