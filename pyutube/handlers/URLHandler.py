
from pyutube.utils import validate_link


class URLHandler:
    def __init__(self, url):
        self.url = url

    def validate(self):
        # Validate the URL and return the result
        return validate_link(self.url)
