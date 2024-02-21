"""
Small example script to demonstrate  the usage of session behind a proxy.
The proxy addresses should be stored in the environment variables HTTP_PROXY and HTTPS_PROXY
"""

import os
from requests_kerberos_proxy.util import get_session

proxies = dict(
    http=os.environ.get("HTTP_PROXY"),
    https=os.environ.get("HTTPS_PROXY"),
)

session = get_session(proxies=proxies)

url = "https://example.com"
request = session.get(url)

print(request.status_code)
