from urllib.parse import urlencode


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

    def get_github_url(self, *args):
        print(self.__getattribute__('login'))
        print(getattr(self, 'login'))
        data={}
        for item in args:
            if hasattr(self,item):
                data[item]=getattr(self,item)
            else:
                print(f'OAuthGitHub中没有{item}属性，已忽略')
        url = 'https://github.com/login/oauth/authorize?' + urlencode(data)
        print(url)
        return url


if __name__ == '__main__':
    a = OAuthGitHub(client_id='d8b3fafc3117d57cdeff', )
    a.get_github_url('client_id','allow_signup')
