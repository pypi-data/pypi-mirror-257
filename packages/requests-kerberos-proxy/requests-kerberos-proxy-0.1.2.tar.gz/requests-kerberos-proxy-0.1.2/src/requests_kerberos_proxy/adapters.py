"""
Class that can be used to overload the HTTP adapter in order to include a proxy
"""

import requests
from urllib3.util import parse_url

import requests_kerberos as rk


class HTTPAdapterWithProxyKerberosAuth(requests.adapters.HTTPAdapter):
    @staticmethod
    def proxy_headers(proxy):
        headers = {}
        auth = rk.HTTPKerberosAuth()
        negotiate_details = auth.generate_request_header(
            None, parse_url(proxy).host, is_preemptive=True
        )
        headers["Proxy-Authorization"] = negotiate_details
        return headers
