from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

def get_args(*args):
  req_json = request.get_json()
  return { arg: req_json.get(arg) for arg in req_json if arg in args }

def api_response(**kwargs):
  return jsonify({ 'message': kwargs.get('msg'), 'data': kwargs.get("data") })

def bad_unpw():
  return api_response(msg="Username or password is incorrect")


def create_app():
  app = Flask(__name__)

  from .db import init_db_command, db, UserModel

  app.config['JWT_SECRET_KEY'] = '$00p3R_$3Cr3t'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
  app.config['DEBUG'] = True
  
  jwt = JWTManager(app)

  db.init_app(app)

  app.cli.add_command(init_db_command)

  @app.route('/register', methods=["POST"])
  def register():
    data = get_args('username', 'password')
    if UserModel.find_by_username(**data):
      return api_response('User "{}" already exists'.format(data['username'])), 400
    new_user = UserModel(
      username=data['username'],
      password=UserModel.generate_hash(data['password'])
    )
    new_user.save_to_db()
    return api_response('user saved', data={'user': new_user.to_json()})

  @app.route('/login', methods=["POST"])
  def login():
    data = get_args('username', 'password')
    user = UserModel.find_by_username(**data)
    if user:
      if UserModel.verify_hash(data['password'], user.password):
        return api_response(
          msg="You've logged in!",
          data=user.to_json()
        ), 200
      return bad_unpw(), 400
    return bad_unpw(), 400

  @app.route('/users')
  def get_users():
    return api_response(data=UserModel.return_all())

  return app


if __name__ == '__main__':
  app = create_app()
  app.run(debug=True, host='0.0.0.0')