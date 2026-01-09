import pytest
from StatHead.models.GameMatchupData import GameMatchupData


def test_parseTeamData_returns_team_ids(parser):
    # This test assumes mockHtml contains a <select id="team_id"> element with <option> children
    html = '''<select id="team_id">
        <option value="">Select Team</option>
        <option value="161">Team A</option>
        <option value="162">Team B</option>
    </select>'''
    team_ids = parser.parseTeamData(html)
    assert team_ids == ["161", "162"]

def test_parseResultTableValueToGameResult_noOvertime(parser):
    result = parser.getGameResultFromTableValue("W 100-99")
    assert result.team_score == 100
    assert result.opp_score == 99
    assert result.result == "W"
    assert result.overtime == 0

def test_parseResultTableValueToGameResult_withOvertime(parser):
    result = parser.getGameResultFromTableValue("L 85-90 (OT)")
    assert result.team_score == 85
    assert result.opp_score == 90
    assert result.result == "L"
    assert result.overtime == 1

def test_parseResultTableValueToGameResult_multipleOvertimes(parser):
    result = parser.getGameResultFromTableValue("W 110-108 (2OT)")
    assert result.team_score == 110
    assert result.opp_score == 108
    assert result.result == "W"
    assert result.overtime == 2


# Split into three tests, one for each game
def test_parseStatPageHtmlString_game1(parser, matchup_game1_html):
    game_data_list = parser.parseStatPageHtmlString(matchup_game1_html)
    assert len(game_data_list) == 1
    game = game_data_list[0]
    assert isinstance(game, GameMatchupData)
    assert game.team_name_abbr == "Alabama"
    assert game.game_location == "HOME"
    assert game.opp_name_abbr == "Mercer"
    assert game.team_score == 101
    assert game.opp_score == 44
    assert game.result == "W"
    assert game.overtime == 0

def test_parseStatPageHtmlString_game2(parser, matchup_game2_html):
    game_data_list = parser.parseStatPageHtmlString(matchup_game2_html)
    assert len(game_data_list) == 1
    game = game_data_list[0]
    assert isinstance(game, GameMatchupData)
    assert game.team_name_abbr == "Alabama"
    assert game.game_location == "NEUTRAL"
    assert game.opp_name_abbr == "Wisconsin"
    assert game.team_score == 71
    assert game.opp_score == 56
    assert game.result == "W"
    assert game.overtime == 0

def test_parseStatPageHtmlString_game3(parser, matchup_game3_html):
    game_data_list = parser.parseStatPageHtmlString(matchup_game3_html)
    assert len(game_data_list) == 1
    game = game_data_list[0]
    assert isinstance(game, GameMatchupData)
    assert game.team_name_abbr == "Minnesota"
    assert game.game_location == "AWAY"
    assert game.opp_name_abbr == "Wisconsin"
    assert game.team_score == 71
    assert game.opp_score == 76
    assert game.result == "L"
    assert game.overtime == 1


def test_parseStatPageHtmlString_endOfOffset_returnsEmptyList(parser, endOfOffsetHtml):
    game_data_list = parser.parseStatPageHtmlString(endOfOffsetHtml)
    assert game_data_list == []