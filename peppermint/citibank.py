import json
import re

from common import Browser, getConfig

username, password = getConfig('citibank.com')
br = Browser.make()

u1 = 'https://online.citibank.com/US/JPS/portal/Home.do'

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
