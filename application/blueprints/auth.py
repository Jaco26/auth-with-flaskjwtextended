from flask import Blueprint
from flask_jwt_extended import jwt_refresh_token_required, create_access_token, create_refresh_token, get_jwt_identity
from application.my_utils import get_args, api_response, bad_unpw
from application.models.user import UserModel

auth_bp = Blueprint("my_auth", __name__)

@auth_bp.route('/register', methods=["POST"])
def register():
  data = get_args('username', 'password')
  if UserModel.find_by_username(**data):
    return api_response('User "{}" already exists'.format(data['username'])), 400
  new_user = UserModel(
    username=data['username'],
    password=UserModel.generate_hash(data['password'])
  )
  try:
    new_user.save_to_db()
    access_token = create_access_token(identity=data['username'])
    refresh_token = create_refresh_token(identity=data['username'])
    return api_response(
      msg="{} has successfully registered!".format(data['username']), 
      data={
        'access_token': access_token,
        'refresh_token': refresh_token,
      }
    ), 201
  except:
    return api_response(msg="Error during registration"), 500

@auth_bp.route('/login', methods=["POST"])
def login():
  data = get_args('username', 'password')
  user = UserModel.find_by_username(**data)
  if user:
    if UserModel.verify_hash(data['password'], user.password):
      return api_response(
        msg="Logged in as {}".format(data['username']),
        data={
          'username': data['username'],
          'access_token': create_access_token(identity=data['username']),
          'refresh_token': create_refresh_token(identity=data['username']),
        }
      ), 200
    return bad_unpw(), 400
  return bad_unpw(), 400

@auth_bp.route('/refresh', methods=["POST"])
@jwt_refresh_token_required
def refresh():
  current_user = get_jwt_identity()
  return api_response(data={'access_token': create_access_token(identity=current_user)})

