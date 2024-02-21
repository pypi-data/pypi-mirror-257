"""
Small example script to demonstrate  the usage of session behind a proxy.
The proxy addresses should be stored in the environment variables HTTP_PROXY and HTTPS_PROXY
"""

import os

import requests

from requests_kerberos_proxy.adapters import HTTPAdapterWithProxyKerberosAuth

proxies = dict(
    http=os.environ.get("HTTP_PROXY"),
    https=os.environ.get("HTTPS_PROXY"),
)

session = requests.Session()
session.proxies = proxies

# kerberos authentication
http_adapter_with_proxy_kerberos_auth = HTTPAdapterWithProxyKerberosAuth()
session.mount("https://", http_adapter_with_proxy_kerberos_auth)

url = "https://example.com"
request = session.get(url)

print(request.status_code)
