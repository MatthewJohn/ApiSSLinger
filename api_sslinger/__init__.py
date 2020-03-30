
import flask
import requests


class ApiSslinger(object):
    """docstring for ApiSslinger"""

    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = '5000'

    IGNORED_HEADERS = [
    	'Content-Length', 'Upgrade-Insecure-Requests']

    def __init__(self):
        """Setup flask app"""
        self.app = flask.Flask(__name__)
        self.app.route('/<path:url>')(self.handle_request)

    def handle_request(self, url):
        """Handle API request"""
        r = requests.request(
            # Copy request method
            flask.request.method,

            # Create https URL
            'https://' + url,

            # Pass headers
            headers=dict(flask.request.headers),
            # ...and data/form data from request
            data=(dict(flask.request.args)
            	  if flask.request.args else
            	  dict(flask.request.form)),

            # Ensure redirects are returned to user
            allow_redirects=False
        )
        print(flask.request.headers)

        # Remove _banned_ headers
        headers = {}
        r_headers = dict(r.headers)
        [headers.update({h: r_headers[h]}) if h not in self.IGNORED_HEADERS else None for h in r_headers]
        print(headers)

        return flask.Response(
            # Passthrough response content, staus code and headers
            response=r.content,
            status=r.status_code,
            headers=headers,
            # This seems necessary, since we writing a bunch
            # of headers that flask will try to set.
            direct_passthrough=True
        )

    def start(self, host=None, port=None, debug=False):
        """Start app."""
        self.app.run(
            host=(host if host else self.DEFAULT_HOST),
            port=(port if port else self.DEFAULT_PORT),
            debug=debug)
