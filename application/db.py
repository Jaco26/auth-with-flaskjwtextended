from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from passlib.hash import pbkdf2_sha256 as sha256
import click

db = SQLAlchemy()

class UserModel(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(80), nullable=False)

  def to_json(self):
    return {
      'id': self.id,
      'username': self.username,
      'password': self.password,
    }

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  @staticmethod
  def generate_hash(password):
    return sha256.hash(password)
  
  @staticmethod
  def verify_hash(password, hash):
    return sha256.verify(password, hash)

  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(username=username).first()

  @classmethod
  def return_all(cls):
    return { 'users': [u.to_json() for u in cls.query.all()] }

  @classmethod
  def delete_all(cls):
    try:
      n_rows_deleted = db.session.query(cls).delete()
      db.session.commit()
      return { 'message': '{} row(s) deleted'.format(n_rows_deleted) }
    except:
      return { 'message': 'something went wrong...'}, 500



@click.command('init-db')
@with_appcontext
def init_db_command():
  db.create_all()