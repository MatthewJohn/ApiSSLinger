#!/usr/bin/env python3

import sys
import os

from api_sslinger import ApiSslinger

server = ApiSslinger()
server.start(
    *sys.argv[1:],
    debug=os.environ.get('DEBUG', False),
    threaded=(os.environ.get('THREADING', True) != 'false'))
