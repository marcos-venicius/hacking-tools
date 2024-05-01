import requests
import json
from cache import Cache

cache = Cache('geo-cache.json')

cache.load()

def geolocate(ip, no_cache=False):
    if no_cache:
        response = requests.get(f'http://ipinfo.io/{ip}/json')

        return json.loads(response.text)

    key = f'GEO-{ip}'

    if key in cache.cache:
        return cache.cache[key]
    else:
        response = requests.get(f'http://ipinfo.io/{ip}/json')

        data = json.loads(response.text)

        cache.cache[key] = data

        cache.write(cache.cache)

        return data

def display_geolocation(result):
    string = []

    if 'hostname' in result:
        string.append('    ' + '\033[1;37mHostname\033[0m'.ljust(25, ' ') + result['hostname'])

    if 'org' in result:
        string.append('    ' + '\033[1;37mOrg\033[0m'.ljust(25, ' ') + result['org'])

    if 'country' in result:
        string.append('    ' + '\033[1;37mCountry\033[0m'.ljust(25, ' ') + result['country'])

    if 'region' in result:
        string.append('    ' + '\033[1;37mRegion\033[0m'.ljust(25, ' ') + result['region'])

    if 'city' in result:
        string.append('    ' + '\033[1;37mCity\033[0m'.ljust(25, ' ') + result['city'])

    if 'timezone' in result:
        string.append('    ' + '\033[1;37mTimezone\033[0m'.ljust(25, ' ') + result['timezone'])

    if 'postal' in result:
        string.append('    ' + '\033[1;37mPostal\033[0m'.ljust(25) + result['postal'])

    if 'loc' in result:
        string.append('    ' + '\033[1;37mCoordinates\033[0m'.ljust(25) + result['loc'])

    if len(string) > 0:
        print('\n'.join(string))

