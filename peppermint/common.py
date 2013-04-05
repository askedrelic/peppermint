import mechanize
import cookielib
import re
import warnings
import ConfigParser
import os

class Browser(object):
    @classmethod
    def make(self):
        # br = mechanize.Browser(
        br = mechanize.Browser(factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True))

        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        br.set_handle_equiv(True)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),
                              max_time=1)

        br.set_debug_http(True)
        br.set_debug_redirects(True)
        br.set_debug_responses(True)

        br.addheaders = [('User-agent',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) '
                        'AppleWebKit/537.31 (KHTML, like Gecko) '
                        'Chrome/26.0.1410.43 Safari/537.31)')]
        return br


def getConfig(site):
    cfg = ConfigParser.ConfigParser()
    try:
        cfg.read(os.path.normpath(os.path.abspath('.') + '/config.ini'))
        username = cfg.get(site, 'username')
    except Exception:
        # try going up once
        cfg.read(os.path.normpath(os.path.abspath('../') + '/config.ini'))
        username = cfg.get(site, 'username')
    return cfg

def getUserPass(site):
    cfg = getConfig(site)
    username = cfg.get(site, 'username')
    password = cfg.get(site, 'password')
    return username, password

def getSecurityQuestions(site):
    cfg = getConfig(site)
    cfg.items('hsabank.com')
    # number/answer lookup
    q = [x[1] for x in cfg.items(site) if x[0].startswith('question')]
    a = [x[1] for x in cfg.items(site) if x[0].startswith('answer')]
    return dict(zip(q,a))


# import difflib
# difflib.get_close_matches(question, qa.keys())
