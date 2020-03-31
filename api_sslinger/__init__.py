
import os
import flask
import requests


class ApiSslinger(object):
    """docstring for ApiSslinger"""

    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = '5000'

    IGNORED_REQ_HEADERS = ['HOST']
    IGNORED_RES_HEADERS = [
        'CONTENT-LENGTH', 'UPGRADE-INSECURE-REQUESTS', 'CONTENT-ENCODING']
    HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

    @property
    def proxies(self):
    	"""Obtain proxies dict config."""
    	proxies = {}
    	https_proxy = os.environ.get('https_proxy', '')
    	if https_proxy:
    		proxies['https'] = https_proxy
    	return proxies

    def __init__(self):
        """Setup flask app"""
        self.app = flask.Flask(__name__)
        self.app.route('/<path:url>', methods=self.HTTP_METHODS)(self.handle_request)

    def handle_request(self, url):
        """Handle API request"""
        # Remove ignored request headers
        u_req_headers = dict(flask.request.headers)
        req_headers = {}
        [req_headers.update({h: u_req_headers[h]}) if h.upper() not in self.IGNORED_REQ_HEADERS else None for h in u_req_headers]

        # Add new host header
        req_headers['Host'] = url.split('/')[0]

        r = requests.request(
            # Copy request method
            flask.request.method,

            # Create https URL
            'https://' + url,

            # Pass headers
            headers=req_headers,
            # ...and data/form data from request
            data=(dict(flask.request.args)
                  if flask.request.args else
                  dict(flask.request.form)),

            # Ensure redirects are returned to user
            allow_redirects=False,

            # Set proxies config
            proxies=self.proxies
        )

        # Remove _banned_ headers.
        # Define response headers and upstream response headers
        res_headers = {}
        u_res_headers = dict(r.headers)
        [res_headers.update({h: u_res_headers[h]}) if h.upper() not in self.IGNORED_RES_HEADERS else None for h in u_res_headers]

        return flask.Response(
            # Passthrough response content, staus code and headers
            response=r.content,
            status=r.status_code,
            headers=res_headers,
            # Add mime-type and content type, if they exist
            mimetype=res_headers.get('Mimetype', None),
            content_type=res_headers.get('Content-Type', None),
            # This seems necessary, since we writing a bunch
            # of headers that flask will try to set.
            direct_passthrough=True
        )

    def start(self, host=None, port=None, debug=False):
        """Start app."""
        self.app.run(
            host=(host if host else self.DEFAULT_HOST),
            port=(port if port else self.DEFAULT_PORT),
            debug=debug,
            threaded=(os.environ.get('THREADING', True) != 'false'))
