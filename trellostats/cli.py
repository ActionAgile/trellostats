import os
import sys
import click

from .models import Snapshot, db_proxy
from .trellostats import TrelloStats
from .helpers import cycle_time, init_db


# Bad, but we're dynamically calling render_ funcs
from .reports import *


@click.group()
@click.pass_context
def cli(ctx):
    """ This is a command line app to get useful stats from a trello board
        and report on them in useful ways.

        Requires the following environment varilables:

        TRELLOSTATS_APP_KEY=<your key here>
        TRELLOSTATS_APP_TOKEN=<your token here>
    """
    ctx.obj = dict()
    ctx.obj['app_key'] = os.environ.get('TRELLOSTATS_APP_KEY')
    ctx.obj['app_token'] = os.environ.get('TRELLOSTATS_APP_TOKEN')
    init_db(db_proxy)


@click.command()
@click.pass_context
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
def resetdb(ctx):
    Snapshot.drop_table(fail_silently=True)
    Snapshot.create_table()
    click.echo('Snapshots table dropped.')


@click.command()
@click.pass_context
def token(ctx):
    ts = TrelloStats(ctx.obj)
    ts.get_token()


@click.command()
@click.pass_context
@click.argument('board')
@click.option('--done', help='Title of column which represents Done\
                              to calc. Cycle Time', default="Done")
def snapshot(ctx, board, done):
    """
        Recording mode - Daily snapshots of a board for ongoing reporting:
         -> trellis report --board=87hiudhw
                          --spend
                          --revenue
                          --done=Done

    """
    ctx.obj['board_id'] = board
    ts = TrelloStats(ctx.obj)
    Snapshot.create_table(fail_silently=True)
    done_id = ts.get_list_id_from_name(done)
    ct = cycle_time(ts, board, done)
    env = get_env()
    print render_text(env, **dict(cycle_time=ct))

    # Create snapshot
    print Snapshot.create(board_id=board, done_id=done_id, cycle_time=ct)


@click.command()
@click.pass_context
@click.argument('board')
@click.option('--done', help='Title of column which represents Done\
                              to calc. Cycle Time', default="Done")
@click.option('--output', type=click.Choice(['html']), default='html', multiple=True)
def report(ctx, board, done, output):
    ctx.obj['board_id'] = board
    ts = TrelloStats(ctx.obj)
    """
        Reporting mode - Daily snapshots of a board for ongoing reporting:
         -> trellis report --board=87hiudhw
                          --spend
                          --revenue
                          --done=Done

    """
    ct = cycle_time(ts, board, done)
    env = get_env()

    #  Get all render functions from the module and filter out the ones we don't want.
    render_functions = [target for target in
                     dir(sys.modules['trellostats.reports'])
                     if target.startswith("render_") and
                     target.endswith(output)]
    
    for render_func in render_functions:
        print globals()[render_func](env, **dict(cycle_time=ct))


@click.command()
@click.pass_context
@click.argument('board')
def test(ctx, board):
    ctx.obj['board_id'] = board
    ts = TrelloStats(ctx.obj)


cli.add_command(snapshot)
cli.add_command(resetdb)
cli.add_command(token)
cli.add_command(report)
cli.add_command(test)