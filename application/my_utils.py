from flask import request, jsonify

def get_args(*args):
  req_json = request.get_json()
  return { arg: req_json.get(arg) for arg in req_json if arg in args }

def api_response(**kwargs):
  return jsonify({ 'message': kwargs.get('msg'), 'data': kwargs.get("data") })

def bad_unpw():
  return api_response(msg="Username or password is incorrect")