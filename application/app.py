from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_current_user

def create_app():
  app = Flask(__name__)

  from .my_utils import get_args, api_response
  from .db import init_db_command, db

  from .models.user import UserModel
  from .models.revoked_token import RevokedToken

  from .blueprints.auth import auth_bp


  app.config['JWT_SECRET_KEY'] = '$00p3R_$3Cr3t'
  app.config['JWT_BLACKLIST_ENABLED'] = True
  app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
  app.config['DEBUG'] = True
  
  jwt = JWTManager(app)
  @jwt.token_in_blacklist_loader
  def is_token_in_blacklist(decryped_token):
    jti = decryped_token.get('jti')
    is_revoked = RevokedToken.is_jti_blacklisted(jti)
    print('IS REVOKEDDDDD?', is_revoked)
    return is_revoked

  db.init_app(app)

  app.cli.add_command(init_db_command)

  app.register_blueprint(auth_bp, url_prefix="/auth")

  @app.route('/protected')
  @jwt_required
  def protected():
    return api_response(msg="Hey you're in!", data={ 'name': 'hi', 'user': get_jwt_identity() }), 200

  @app.route('/users')
  def get_users():
    return api_response(data=UserModel.return_all())

  return app
