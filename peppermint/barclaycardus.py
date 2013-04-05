import re
from BeautifulSoup import BeautifulSoup

from common import Browser, getConfig, getUserPass, getSecurityQuestions

site = 'barclaycardus.com'
username, password = getUserPass(site)
qa = getSecurityQuestions(site)
br = Browser.make()

u1 = 'https://www.barclaycardus.com/'
r1 = br.open(u1)

# form infos
# print [x.attrs for x in br.forms()]

# # controls
# print [x.attrs for x in f.controls for f in br.forms()]
print br.geturl()

br.select_form(nr=0)
br['userId'] = username
r2 = br.submit()
r2_text = r2.read()

# hmmm fix up some shitty JS causing parse error
r2_text = r2_text.replace('<!")','')
r2.set_data(r2_text)
br.set_response(r2)

br.select_form(nr=0)
br.set_all_readonly(False)
#set remember device, meh?
# br['registerDevice'] = 'true'
# br.form.set_value(['true'], name='registerDevice')

if 'Enter Your Password' not in r2_text:
    #register PC
    soup = BeautifulSoup(r2_text)
    questions = [x.text for x in soup.findAll('span', {'class': 'formLabel'}) if 'username' not in x.text.lower() and 'register' not in x.text.lower()]
    answers = ['answer1', 'answer2']

    for question, answer in zip(questions,answers):
        if question in qa:
            print 'using config answer for security question'
            br[answer] = qa[question]
            print '%s : %s' % (question , qa[question])
        else:
            print 'MISSING config answer for security question'
            br[answer] = raw_input('%s: ' % question)

    r3 = br.submit()
    r3_text = r3.read()

    # hmmm fix up some shitty JS causing parse error
    r3_text = r3_text.replace('<!")','')
    r3.set_data(r3_text)
    br.set_response(r3)

br.select_form(nr=0)
br['password'] = password

r4 = br.submit()
r4_text = r4.read()

soup = BeautifulSoup(r4_text)
money = [x.text for x in soup.find(id='row1a').findAll('h1', {'class': None})]

accountData = {
    'current_balance': money[0],
    'statement_balance': money[1],
    'available_credit': money[2],
    'revolving_credit_line': money[3],
}
accountName = [x.text for x in soup.findAll('h1', {'class': 'cardName'})][0]
accountId = re.findall(r'Card ending in (\d{4})', r4_text, re.IGNORECASE)[0]

print accountName
print accountId
print accountData

import IPython; IPython.embed()
