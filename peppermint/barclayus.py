import ConfigParser
import os
import re

from common import Browser, getConfig

username, password = getConfig('citibank.com')
br = Browser.make()

def foo():
    print 'foo'
