class OAuthGitHub(object):
    def __init__(
            self, client_id, client_secret, redirect_uri=None, state=None, login=None, scope=None,
            allow_signup=False
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.login = login
        self.scope = scope
        self.state = state
        self.allow_signup = allow_signup
