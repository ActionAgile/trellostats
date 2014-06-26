import pytest
from mock import Mock, MagicMock, patch

import trellostats
from trellostats.charts import get_snapshots_for_boards, render_cycle_time_history_chart


@patch('trellostats.charts.Snapshot')
def test_get_snapshots_for_boards(mock_snapshot):
    get_snapshots_for_boards(Mock())
    assert mock_snapshot.select.called


@patch('trellostats.charts.pygal.Line')
@patch('trellostats.charts.get_snapshots_for_boards')
def test_render_cycle_time_history(mock_pygal, mock_snapshot):
	mock_board = Mock()
	render_cycle_time_history_chart(mock_board)
	assert mock_pygal.title.called_once_with('Cycle Time')
	assert mock_snapshot.called_once_with(mock_board)