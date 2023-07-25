import requests
from bs4 import BeautifulSoup

"""
support methods to be used by main methods
"""

MAX_CALLS = 10

def getSoup(url):
    """
    get soup from url
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup