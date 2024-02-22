
import requests
import logging

from promium.base import Element
from promium.helpers import ParseUrl


log = logging.getLogger(__name__)


class Link(Element):

    @property
    def href(self):
        return self.get_attribute("href")

    @property
    def parse_url(self):
        """
        Using parse_url to parse href. Can get attributes:
        - scheme
        - host
        - sub_domain
        - port
        - path
        - params
        - query
        - fragment
        - product_id
        """
        return ParseUrl(self.href)

    @property
    def response(self):
        session = requests.Session()
        for cookie in self.driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])
        for i in range(1, 3):
            r = session.get(self.href, verify=False, timeout=10)
            if r.status_code in [502, 503, 504] and r.request.method == 'GET':
                log.warning(f'[Request Retry]: attempt:{i}, status: {r.status}')
            else:
                break

        return r

    @property
    def get_status_code(self):
        """Gets status requests code from link"""
        return self.response.status_code
