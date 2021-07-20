import unittest
from fetchData import *


class TestFetchData(unittest.TestCase):
    def testGetDataFailure(self):
        """ Test that when it is unable to get data for the url """
        url: str = "www.google.com"
        result: str = getData(url)
        self.assertFalse(result)

    def testGetDataSuccess(self):
        """Test when data can be gotten from the url"""
        url: str = "https://en.wikipedia.org/wiki/Road_safety_in_Europe"
        result: str = getData(url)
        self.assertTrue(result)

    def testParseHTMLFailure(self):
        """Test when parse response in parse HTML method is empty"""
        response: Optional[str] = None
        result: str = parseHtml(response)
        self.assertFalse(result)

