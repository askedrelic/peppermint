import mechanize
import cookielib
import json
from BeautifulSoup import BeautifulSoup

from common import Browser, getConfig, getUserPass, getSecurityQuestions

site = 'hsabank.com'
username, password = getUserPass(site)
qa = getSecurityQuestions(site)
br = Browser.make()

u1 = 'https://secure.hsabank.com/ibanking3/login.aspx'

r1 = br.open(u1)
r1_text = r1.read()

#are we at the correct url?
sanity_check = "Log in to Your Account" in r1_text

br.select_form(nr=0)
br['ctl00$IbankingPlaceHolder$txtUserId'] = username
br['ctl00_IbankingPlaceHolder_txtUserId_text'] = username
#readonly forms
br.set_all_readonly(False)
br['ctl00_IbankingPlaceHolder_txtUserId_ClientState'] = '{"enabled":true,"emptyMessage":"Enter User Name"}'
br['pm_fp'] = """version%3D1%26pm%5Ffpua%3Dmozilla%2F5%2E0%20%28macintosh%3B%20intel%20mac%20os%20x%2010%5F8%5F3%29%20applewebkit%2F537%2E31%20%28khtml%2C%20like%20gecko%29%20chrome%2F26%2E0%2E1410%2E43%20safari%2F537%2E31%7C5%2E0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010%5F8%5F3%29%20AppleWebKit%2F537%2E31%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F26%2E0%2E1410%2E43%20Safari%2F537%2E31%7CMacIntel%26pm%5Ffpsc%3D24%7C1680%7C1050%7C1028%26pm%5Ffpsw%3D%26pm%5Ffptz%3D%2D8%26pm%5Ffpln%3Dlang%3Den%2DUS%7Csyslang%3D%7Cuserlang%3D%26pm%5Ffpjv%3D1%26pm%5Ffpco%3D1"""

r2 = br.submit()
r2_text = r2.read()
# import IPython; IPython.embed()

if 'not logging on from a computer registered' in r2_text:
    print 'On register computer step'

# find challenge question
soup = BeautifulSoup(r2_text)
s = soup.findAll('span', id=lambda x: x and x.startswith('ChallengeQuestionLabel'))[0]
question = s.getText()

br.select_form(nr=0)
br.set_all_readonly(False)
br.form.set_value(['RdoYes'], name='ctl00$IbankingPlaceHolder$RegisterComputerRadioGroup')
# this might not be required
br['__EVENTTARGET'] = 'ctl00$IbankingPlaceHolder$BtnContinue'
br['RadScriptManager1_TSM'] = ';;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:89093640-ae6b-44c3-b8ea-010c934f8924:ea597d4b:b25378d2;Telerik.Web.UI:en-US:f9722142-3e1c-4803-86df-ecfc0d24f144:16e4e7cd:f7645509:22a6274a'
# think this required too
br.addheaders = [('Origin', 'https://secure.hsabank.com')]

if question in qa:
    print 'using config answer for security question'
    answer = qa[question]
    print '%s : %s' % question , answer
else:
    print 'MISSING config answer for security question'
    answer = raw_input('%s: ' % question)

br['ctl00$IbankingPlaceHolder$AnswerText'] = answer
# import IPython; IPython.embed()

r3 = br.submit()
r3_text = r3.read()
# import IPython; IPython.embed()

#should be at password stage
br.select_form(nr=0)
br.set_all_readonly(False)
if "ctl00$IbankingPlaceHolder$PasswordText" in r3_text:
    print 'looks like password stage'
else:
    print 'something went wrong r3'
br['ctl00$IbankingPlaceHolder$PasswordText'] = password
br['RadScriptManager1_TSM'] = ';;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:89093640-ae6b-44c3-b8ea-010c934f8924:ea597d4b:b25378d2;Telerik.Web.UI:en-US:f9722142-3e1c-4803-86df-ecfc0d24f144:16e4e7cd:f7645509:22a6274a'

r4 = br.submit()
r4_text = r4.read()

if "Change Login Password" in r3_text:
    print 'looks like change password every 90 days stage'
# else:
#     print 'something went wrong r4'
# import IPython; IPython.embed()

soup = BeautifulSoup(r4_text)
tr = soup.findAll('tr', id=lambda x: x and x.startswith('ctl00_IbankingPlaceHolder_accountGrid_ctl00__0'))[0]
print tr.findAll('td')

# try scraping transactions?
# https://secure.hsabank.com/ibanking3/Accounts/transactions.aspx
#
# http://stackoverflow.com/questions/4720470/using-python-and-mechanize-to-submit-form-data-and-authenticate
