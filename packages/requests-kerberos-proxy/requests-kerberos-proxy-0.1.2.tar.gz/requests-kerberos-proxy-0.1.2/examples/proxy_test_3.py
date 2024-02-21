"""
Small example script to demonstrate  the usage of session behind a proxy.
The proxy addresses should be stored in the environment variables HTTP_PROXY and HTTPS_PROXY
In this example we don't pass the proxies as an argument, but let is to the function to get them
"""
from requests_kerberos_proxy.util import get_session

session = get_session()

url = "https://example.com"
request = session.get(url)

print(request.status_code)
