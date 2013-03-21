import mechanize
import cookielib
import json

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
     'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US)'
     'AppleWebKit/534.10 (KHTML, like Gecko)'
     'Chrome/8.0.552.11 Safari/534.10')]

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

br['username'] = ''

br['password'] = ''

br.submit()

r2 = br.open('https://online.citibank.com/US/REST/accountsPanel/getCustomerAccounts.jws?ttc=742', data={})
d = json.loads(r2.read())

print d
