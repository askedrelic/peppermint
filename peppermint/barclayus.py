import re
from BeautifulSoup import BeautifulSoup

from common import Browser, getConfig, getUserPass, getSecurityQuestions

username, password = getConfig('citibank.com')
br = Browser.make()

def foo():
    print 'foo'
