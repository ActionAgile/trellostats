import pygal
from .models import Snapshot
from pygooglechart import SimpleLineChart

def get_snapshots_for_boards(board):
	return [(s.when, s.cycle_time) for s in Snapshot.select().where(Snapshot.board_id == board)]


def render_cycle_time_history_chart(board):
	line_chart = pygal.Line()
	line_chart.title = 'Cycle Time'
	history = get_snapshots_for_boards(board)
	chart = SimpleLineChart(800, 300, y_range=(0, 100))
	# , y_range=(min(history), max(history))) 
	print [ct[1] for ct in history]
	import random
	chart.add_data([random.randrange(0, 20) for x in range(100)])
	print dir(chart)
	print chart.get_url()
	chart.download('mych.png')
