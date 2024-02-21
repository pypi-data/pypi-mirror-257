from requests import Session

from requests_kerberos_proxy.util import get_session

__author__ = "EVLT"
__copyright__ = "EVLT"
__license__ = "MIT"


def test_session():
    """Type Tests"""
    session = get_session()
    assert isinstance(session, Session)


