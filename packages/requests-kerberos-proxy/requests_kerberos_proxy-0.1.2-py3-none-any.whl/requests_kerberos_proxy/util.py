import os

import requests
from requests import Session

from .adapters import HTTPAdapterWithProxyKerberosAuth


def get_session(proxies=None) -> type(Session):
    session: Session = requests.Session()
    if proxies is None:
        # proxies not given via arguments. Try to get them via environment variables
        proxies = {}
        if http_proxy := os.environ.get("HTTP_PROXY"):
            proxies["http"] = http_proxy
        if https_proxy := os.environ.get("HTTPS_PROXY"):
            proxies["https"] = https_proxy

    if proxies:
        session.proxies = proxies
        # kerberos authentication
        http_adapter_with_proxy_kerberos_auth = HTTPAdapterWithProxyKerberosAuth()
        session.mount("https://", http_adapter_with_proxy_kerberos_auth)

    return session
