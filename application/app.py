from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required

def create_app():
  app = Flask(__name__)

  from .my_utils import get_args, api_response
  from .db import init_db_command, db

  from .models.user import UserModel

  from .blueprints.auth import auth_bp


  app.config['JWT_SECRET_KEY'] = '$00p3R_$3Cr3t'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
  app.config['DEBUG'] = True
  
  jwt = JWTManager(app)

  db.init_app(app)

  app.cli.add_command(init_db_command)

  app.register_blueprint(auth_bp, url_prefix="/auth")

  @app.route('/protected')
  @jwt_required
  def protected():
    return api_response(msg="Hey you're in!", data={ 'name': 'hi' }), 200

  @app.route('/users')
  def get_users():
    return api_response(data=UserModel.return_all())

  return app


if __name__ == '__main__':
  app = create_app()
  app.run(debug=True, host='0.0.0.0')