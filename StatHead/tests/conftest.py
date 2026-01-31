import pytest
import sys
import os

#TODO: find a better way to import modules than this
#found, look at test_parser file
sys.path.append("../..")
sys.path.append("..")
from StatHead.statheadParser import Parser


# Fixtures for each individual game row html
@pytest.fixture()
def matchup_game1_html():
    with open("models/matchup_game1.html", "r") as f:
        html = f.read()
    return html

@pytest.fixture()
def matchup_game2_html():
    with open("models/matchup_game2.html", "r") as f:
        html = f.read()
    return html

@pytest.fixture()
def matchup_game3_html():
    with open("models/matchup_game3.html", "r") as f:
        html = f.read()
    return html

@pytest.fixture()
def endOfOffsetHtml():
    html = str
    with open("models/endOfOffsetPage.html", "r") as f:
        html = f.read(),
    f.close()
    return html[0]

@pytest.fixture
def parser():
    return Parser()

