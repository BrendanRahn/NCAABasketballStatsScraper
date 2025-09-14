import pytest
import sys
import os
sys.path.append("..")
from ncaabasketballstatsscraper.Parser import Parser

@pytest.fixture()
def mockHtml():
    html = str
    path = os.getcwd() + "\\tests\\models\\mock_html.html"
    with open("models/mock_html.html", "r") as f:
        html = f.read(),
    f.close()
    return html[0]

@pytest.fixture
def parser():
    return Parser()

