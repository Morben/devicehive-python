class Request(object):
    """Request class."""

    def __init__(self, url, action, request, **params):
        self.action = action
        self.request = request
        self.params = params
        self.params['url'] = url


class Response(object):
    """Response class."""

    def __init__(self, response):
        self.action = response.pop('action')
        self.is_success = response.pop('status') == 'success'
        self.code = response.pop('code', None)
        self.error = response.pop('error', None)
        self.data = response


class Api(object):
    """Api class."""

    def __init__(self, transport):
        self._transport = transport

    def _is_http_transport(self):
        return self._transport.name == 'http'

    def _is_websocket_transport(self):
        return self._transport.name == 'websocket'

    def _request(self, url, action, request, **params):
        req = Request(url, action, request, **params)
        resp = self._transport.request(req.action, req.request, **req.params)
        return Response(resp)


class Token(Api):
    """Token class."""

    def __init__(self, transport, authentication):
        Api.__init__(self, transport)
        self._login = authentication.get('login')
        self._password = authentication.get('password')
        self._refresh_token = authentication.get('refresh_token')
        self._access_token = authentication.get('access_token')
        self._authenticate_params = {}

    def _login(self):
        # TODO: implement token/login request.
        # Set self._refresh_token and self._access_token after success login.
        pass

    def _authenticate(self):
        if self._is_websocket_transport():
            url = None
            action = 'authenticate'
            request = {'token': self._access_token}
            params = {}
            response = self._request(url, action, request, **params)
            assert response.is_success, 'Authentication failure'
            return
        headers = {'Authorization': 'Bearer ' + self._access_token}
        self._authenticate_params['headers'] = headers

    def access_token(self):
        return self._access_token

    def authenticate_params(self):
        return self._authenticate_params

    def refresh(self):
        url = 'token/refresh'
        action = url
        request = {'refreshToken': self._refresh_token}
        params = {'method': 'POST', 'merge_data': True}
        response = self._request(url, action, request, **params)
        assert response.is_success, 'Token refresh failure'
        self._access_token = response.data['accessToken']

    def authenticate(self):
        if self._refresh_token:
            self.refresh()
        else:
            self._login()
        self._authenticate()
