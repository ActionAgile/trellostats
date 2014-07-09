import pytest
from mock import Mock, MagicMock, patch
from trellostats.models import Snapshot

def test_repr():
	s = Snapshot(board_id='hi', cycle_time=1)
	assert repr(s) == '<Snapshot:hi:1>'
