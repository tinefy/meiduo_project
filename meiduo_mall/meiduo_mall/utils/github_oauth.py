# from urllib.parse import urlencode
from django.utils.http import urlencode


class OAuthGitHub(object):
    def __init__(
            self, client_id=None, client_secret=None, redirect_uri=None, state=None, login=None, scope=None,
            allow_signup='true'
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        # self.login = login
        self.login = 'login'
        self.scope = scope
        self.state = state
        self.allow_signup = allow_signup

    def get_github_url(self,*args):
        print(self.__getattribute__('login'))
        print(getattr(self,'login'))
        data = {
            'client_id': self.client_id,
            # 'state': self.state,
            'allow_signup': self.allow_signup
        }
        url = 'https://github.com/login/oauth/authorize?' + urlencode(data)
        print(url)
        return url



if __name__ == '__main__':
    a =OAuthGitHub(client_id='d8b3fafc3117d57cdeff',)
    a.get_github_url()

