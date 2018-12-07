from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = '3ncl20fnd3o95'
jwt = JWTManager(app)

@app.route('/', methods=["GET"])
def login():
  return 'Hi'


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')