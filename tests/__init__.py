import os
import sys
import shortuuid

sys.path.insert(0, os.path.join(os.pardir, 'trellostats'))


from peewee import SqliteDatabase
from trellostats.models import Snapshot, db_proxy

# Initilise in memory database and some data points
db_proxy.initialize(SqliteDatabase(':memory:'))
Snapshot.create_table()

for x in range(100):
	Snapshot.create(**dict(board_id=shortuuid.uuid(), cycle_time=x*10, done_id=shortuuid.uuid()))
