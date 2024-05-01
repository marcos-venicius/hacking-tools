import re

def ip_is_valid(ip):
    pattern = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")

    return pattern.match(ip)
