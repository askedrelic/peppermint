import re
from BeautifulSoup import BeautifulSoup

from common import Browser, getConfig, getUserPass, getSecurityQuestions

def main():
    site = 'onlinecreditcenter6.com'
    username, password = getUserPass(site)
    qa = getSecurityQuestions(site)
    br = Browser.make()

    u1 = 'https://www3.onlinecreditcenter6.com/consumergen2/login.do?subActionId=1000&clientId=br&accountType=plcc'
    r1 = br.open(u1)
    print '1'

    # where am i!
    print br.geturl()

    # form infos
    print [x for x in br.forms()]

    # controls
    # print [x.pairs() for x in br.form.controls]

    br.select_form(nr=0)
    br.set_all_readonly(False)
    br['userId'] = username
    #bullshit values
    br['devicePrint'] = 'version=1&pm_fpua=mozilla/5.0 (macintosh; intel mac os x 10.8; rv:20.0) gecko/20100101 firefox/20.0|5.0 (Macintosh)|MacIntel&pm_fpsc=24|1680|1050|1024&pm_fpsw=&pm_fptz=-8&pm_fpln=lang=en-US|syslang=|userlang=&pm_fpjv=1&pm_fpco=1'
    br['subActionId'] = '6101'
    br['counterror'] = '0'
    br.form.set_value(['on'], name='rememberMeFlag')
    r2 = br.submit()
    print '2'
    r2_text = r2.read()

    # hmmm fix up some shitty JS causing parse error
    r2.set_data(r2_text.replace('<! --',''))
    br.set_response(r2)
    

    br.select_form(nr=0)
    print [x.pairs() for x in br.form.controls]
    br.set_all_readonly(False)

    # import IPython; IPython.embed()

    #register PC step
    if 'strChallengeQuestion' in [x.name for x in br.controls]:
        question = br['strChallengeQuestion']
        answer = 'challengeAnswer1'
        if question in qa:
            print 'using config answer for security question'
            br[answer] = qa[question]
            print '%s : %s' % (question , qa[question])
        else:
            print 'MISSING config answer for security question'
            br[answer] = raw_input('%s: ' % question)

        r3 = br.submit()
        print 3
        r3_text = r3.read()


    br.select_form(nr=0)
    br['password'] = password
    r4 = br.submit()
    r4_text = r4.read()
    print 4

    if 'Account Summary' in r4_text:
        print 'success!'

    soup = BeautifulSoup(r4_text)
    accountData = {
        'current_balance':       float(soup.find(id='currentBalance').text),
        'statement_balance':     float(soup.find(id='lastStmtBalance').text),
        'available_credit':      float(soup.find(id='availableCredit').text),
        'revolving_credit_line': float(soup.find(id='avlReserve').text),
    }


    #the only card type?
    accountName = 'Banana Republic Visa Card'
    accountId = re.findall(r'Account ending in\s*(\d{4})', r4_text, re.IGNORECASE)

    print accountName
    print accountId
    print accountData

if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except Exception as e:
    #     import ipdb; ipdb.set_trace();
        # import IPython; IPython.embed()
