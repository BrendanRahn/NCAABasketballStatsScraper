import json
import os
#TODO: Make parser import from parent directory
from ncaabasketballstatsscraper.Parser import Parser


class MockData:
    def mockHtml():
        html = str
        path = os.getcwd() + "\\tests\\models\\mock_html.html"
        with open(path, "r") as f:
            html = f.readlines(),
        f.close()
        return html
    
@pytest.fixture
def parser():
    return Parser()

def test_getData_returnsData(parser):
    mockData =  MockData.mockHtml()
    res = parser.getData(mockData)
    return res

test_getData_returnsData()