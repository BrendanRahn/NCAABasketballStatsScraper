import json
import os
import sys
import pytest

def test_getData_returnsData(parser, mockHtml):
    res = parser.getData(mockHtml)
    assert res == [['32', 'N Florida', '83.2', '87.0', '81.0', '84.7', '82.6', '75.6'],
                   ['34', 'Georgia', '83.1', '80.7', '100.0', '89.9', '71.3', '74.7'],
                   ['37', 'PJ Hall', 'Clemson Tigers', 'C', '0.61'],
                   ['38', 'Tayton Conerway', 'Troy Trojans', 'G', '0.61']]

def test_getData_dataHasNonNumbericChars_sanitizesData(parser):
    unsanitizedMockHtml = "<tbody><tr><td>1</td><td>Samson Johnson</td><td>Connecticut Huskies</td><td>C</td><td>76.6%</td></tr></tbody>"
    data = parser.getData(unsanitizedMockHtml)
    parsedData = parser.sanitizeData(data[0])
    assert parsedData == ['1', 'Samson Johnson', 'Connecticut Huskies', 'C', '76.6']

def test_getParamValues_returnsParamValues(parser):
    url = 'https://example.com/page?param1=value1&param2=value2&param3=value3'
    res = parser.getParamsAndValuesDict(url)
    assert res == {
        'param1': 'value1',
        'param2': 'value2',
        'param3': 'value3'
    }

def test_getPlayerSchemaName_returnsPlayerSchemaName(parser):
    url = 'https://example.com/player-stat/page?param1=value1&param2=value2&param3=value3'
    res = parser.getSchemaName(url)
    assert res == 'player'

def test_getTeamSchemaName_returnsTeamSchemaName(parser):
    url = 'https://example.com/page?param1=value1&param2=value2&param3=value3'
    res = parser.getSchemaName(url)
    assert res == 'team'
