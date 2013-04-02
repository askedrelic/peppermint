import mechanize
import cookielib
import json
import ConfigParser
import os
import re

cfg = ConfigParser.ConfigParser()
cfg.read(os.path.normpath(os.path.abspath('.') + '/config.ini'))

username = cfg.get('citibank.com', 'username')
password = cfg.get('citibank.com', 'password')

u1 = 'https://online.citibank.com/US/JPS/portal/Home.do'

br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.addheaders = [('User-agent',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) '
                  'AppleWebKit/537.31 (KHTML, like Gecko) '
                  'Chrome/26.0.1410.43 Safari/537.31)')]

# br.addheaders = [('User-agent',
#      'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US)'
#      'AppleWebKit/534.10 (KHTML, like Gecko)'
#      'Chrome/8.0.552.11 Safari/534.10'), ('X-Requested-With', 'XMLHttpRequest')]

br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

r1 = br.open(u1)

print br.geturl()

print [x.attrs for x in br.forms()]

br.select_form(nr=2)

br['username'] = username
br['password'] = password 

br.submit()

r2 = br.open('https://online.citibank.com/US/REST/accountsPanel/getCustomerAccounts.jws?ttc=742', data={})
d = json.loads(r2.read())

kill_tags = re.compile(r'<.*?>')
kill_double_space = re.compile(r'\s+')
def format_label(label):
    label = kill_tags.sub('',label)
    label = label.replace(':','')
    return label.replace(' ', '_').lower()

def format_value(value):
    value = value.replace('$','').replace(' ', '').replace(',','')
    return float(value)

cardData = {format_label(x['label']) : format_value(x['value']) for x in d['accountsSummaryViewObj']['categoryList'][0]['products'][0]['accountBalViewObjList']}

accountName = d['accountsSummaryViewObj']['categoryList'][0]['products'][0]['accountName']
accountName = kill_tags.sub(' ', accountName)
accountName = kill_double_space.sub(' ', accountName).replace('Citi &reg;', '').strip()

print accountName
print cardData
