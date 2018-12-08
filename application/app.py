from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

def get_args(req, *args):
  return { arg for arg in req.get_json() if arg in args}


def create_app():
  app = Flask(__name__)

  from .db import init_db_command, db

  app.config['JWT_SECRET_KEY'] = '$00p3R_$3Cr3t'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
  app.config['DEBUG'] = True
  
  jwt = JWTManager(app)

  db.init_app(app)

  app.cli.add_command(init_db_command)

  @app.route('/register', methods=["POST"])
  def register():
    password, username = get_args(request, 'username', 'password').values()
    print('password', password, 'username', username)


  @app.route('/hi', methods=["GET"])
  def login():
    print('hello')
    return jsonify({'msg': 'Hi'})

  return app


if __name__ == '__main__':
  app = create_app()
  app.run(debug=True, host='0.0.0.0')