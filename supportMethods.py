import requests
from bs4 import BeautifulSoup

"""
support methods to be used by main methods
"""

def getSoup(url):
    """
    get soup from url
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup