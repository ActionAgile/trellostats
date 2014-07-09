import pytest
from mock import Mock, MagicMock, patch

import trellostats
from trellostats import TrelloStats
from trellostats.settings import TOKEN_URL, LIST_URL, BOARD_URL
from trellostats.trellostats import TrelloStatsException
from requests.exceptions import ConnectionError


@pytest.fixture
def ts_obj():
    mock_context = dict(app_key=Mock(), app_token=Mock(), board_id=Mock())
    return TrelloStats(mock_context)


@patch('trellostats.TrelloStats.get_lists')
def test_get_list_id_from_name_works(mock_get_lists, ts_obj):
    mock_get_lists.return_value = [{'id': 'eh23jnd2', 'name': 'Thang'}]
    list_id = ts_obj.get_list_id_from_name("Thang")
    assert list_id == 'eh23jnd2'


@patch('trellostats.TrelloStats.get_lists')
def test_get_list_id_from_name_is_none_with_nonexistent_name(mock_get_lists,
                                                             ts_obj):
    mock_get_lists.return_value = [{'id': 'eh23jnd2', 'name': 'Thang'}]
    list_id = ts_obj.get_list_id_from_name("NotThang")
    assert not list_id


@patch('requests.get')
def test_get_lists(mock_get, ts_obj):
    ts_obj.get_lists()
    mock_get.assert_called_with(BOARD_URL.format(ts_obj.board_id,
                                                          ts_obj.app_key,
                                                          ts_obj.app_token))

@patch('requests.get')
def test_get_noneexisitent_done_board_returns_trellostatserror(mock_get, ts_obj):
    with pytest.raises(TrelloStatsException):
        mock_get.side_effect = ValueError
        list_id = ts_obj.get_list_id_from_name("Thang")
    

@patch('requests.get')
def test_no_connection_board_returns_trellostatserror(mock_get, ts_obj):
    with pytest.raises(TrelloStatsException):
        mock_get.side_effect = ConnectionError
        list_id = ts_obj.get_list_id_from_name("Thang")


@patch('trellostats.trellostats.webbrowser')
def test_get_token_opens_browser_with_right_token(mock_web, ts_obj):
    ts_obj.get_token()
    mock_web.open.assert_called_once_with(TOKEN_URL.format(ts_obj.app_key))


@patch('trellostats.requests.get')
def test_get_list_data(mock_get, ts_obj):
    ts_obj.get_list_data('listylist')
    mock_get.assert_called_with(LIST_URL.format('listylist',
                                                         ts_obj.app_key,
                                                         ts_obj.app_token))


@patch('trellostats.grequests.map')
def test_get_history_for_cards(mock_g, ts_obj):
    ts_obj._get_history_for_cards(MagicMock(spec=dict))
    assert mock_g.called


def test_repr(ts_obj):
    assert repr(ts_obj).startswith('<TrelloStats')
