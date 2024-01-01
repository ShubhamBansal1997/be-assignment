import requests
import logging
import uuid
from lxml.html import document_fromstring, tostring
import sys


logger = logging.getLogger('scraper')
logger.setLevel(logging.DEBUG)

class Scraper(object):
    def __init__(self, url):
        self.request_id = str(uuid.uuid4())
        self.url = url
        self.root = None

    def set_root(self, response_text):
        try:
            self.root = document_fromstring(response_text)
        except ValueError:
            logger.exception(f"[{self.request_id}]: Unable to load the request response")

    def get_title(self):
        try:
            title = self.root.findtext(".//title")
            return title
        except Exception as e:
            logger.exception(f"[{self.request_id}]: Exception in the getting the title {str(e)}")

    def get_meta_description(self):
        meta_description = self.root.xpath('//meta[@name="description"]/@content')
        if meta_description:
            meta_description = meta_description[0]
        else:
            meta_description = ""
        return meta_description

    def get_content_length(self):
        content_length = len(tostring(self.root))
        return content_length

    def store_in_s3(self, response_text):
        # Store the response text in the S3
        # Used for debugging
        pass

    def fetch_content(self):
        # Fetch content here is very basic
        # Going forward this function can be transformed into itself a package or process
        # Why?
        # In scraping website multiple cases exists, you need something extra
        # - Sometimes proxies (paid/free)
        # - Sometimes websites block crawlers based on user-agent
        # - Sometimes selenium
        # etc.....
        try:
            response = requests.get(self.url, timeout=60)
            if response.status_code == 200:
                self.store_in_s3(response.content)
                self.set_root(response.content)
            else:
                raise Exception(f"[{self.request_id}]: Unable to fetch the URL {self.url}")
        except Exception as e:
            logger.exception(f"[{self.request_id}]: Exception in the fetch Content {str(e)}")

    def process(self):
        try:
            self.fetch_content()
            data = {
                "request_id": self.request_id,
                "url": self.url,
                "title": self.get_title(),
                "meta_description": self.get_meta_description(),
                "content_length": self.get_content_length(),
            }
            return data
        except Exception as e:
            logger.exception(f"[{self.request_id}]: Exception while processing {str(e)}")


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            logger.error("Please provide the url")
        else:
            url = sys.argv[1]
            crawler = Scraper(url)
            output = crawler.process()
            print("output", output)
    except Exception as e:
        logger.exception(f"Exception while processing {str(e)}")

