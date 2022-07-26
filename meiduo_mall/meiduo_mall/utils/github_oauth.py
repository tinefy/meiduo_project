from urllib.parse import urlencode
from requests import get


class OAuthGitHub(object):
    def __init__(
            self, client_id=None, client_secret=None, redirect_uri=None, state=None, login=None, scope=None,
            allow_signup='true'
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.login = login
        self.scope = scope
        self.state = state
        self.allow_signup = allow_signup

        self.url = ''

    def get_github_url(self, *args):
        data = {}
        if not args:
            for key, value in vars(self).items():
                if value:
                    data[key] = value
        else:
            for item in args:
                if hasattr(self, item):
                    data[item] = getattr(self, item)
                else:
                    print(f'OAuthGitHub中没有{item}属性，已忽略')
        self.url = 'https://github.com/login/oauth/authorize?' + urlencode(data)
        return self.url

    def get_temporary_code(self, url=None):
        if url:
            self.url = url
        get(url)


if __name__ == '__main__':
    a = OAuthGitHub(client_id='d8b3fafc3117d57cdeff')
    a.get_github_url('client_id', 'allow_signup')
