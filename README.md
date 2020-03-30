

# API SSLinger

Slinging SSL round HTTP calls

API Proxy to provide SSL wrapper to upstream APIs. Useful for older applications that do not support modern TLS standards (e.g. TLS 1.2)


## Example

curl http://localhost:5000/api.google.com/api/v3/some-awesome-api -H 'AllHeadersGet: PassedOn' -d 'As well as any data (and method...)' -XPOST

Result: HTTPS call to api.google.com.


## Quickstart

### Install

    virtualenv -p python3 .
    . ./bin/activate
    pip install -r requirements.txt


### Start

    python3 ./server.py


### Usage

    python3 ./server.py <Host> <Port>


### Environment variables

* `DEBUG` - Set to 'true' to enable debug (default: disabled)
* `THREADING` - Set to 'false' to disable (defaults on)
* `https_proxy` - Set to upstream https proxy (default: '')


## Notes

This is _only_ meant for APIs, as general websitess have a lot of (absolute) relative paths that do not work, as well as redirects etc.


## Recommended Music

* Gunslinga - Pegbaord Nerds - https://www.youtube.com/watch?v=vIaPWxMPhug


## Quotes

* `You yellow-bellied, lily-livered, API-sslingin'... draw!` - Phoebe, Friends (27. March 1997)
