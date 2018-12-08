from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import click

db = SQLAlchemy()

@click.command('init-db')
@with_appcontext
def init_db_command():
  db.create_all()