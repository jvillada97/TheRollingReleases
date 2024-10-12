from flask import request, Blueprint
import os
from flask.json import jsonify
from commands.add import AddEmail
from errors.errors import ApiError, NotToken, TokenInvalid

emails_blueprint = Blueprint('emails', __name__)

@emails_blueprint.route('/blacklists', methods=['POST'])
def add():
    authorization_token = request.headers.get('Authorization')
    data = request.get_json()
    client_ip = request.remote_addr
    token = None
    if authorization_token is not None:
        token = authorization_token.replace('Bearer ', '')
    else:
        raise NotToken
    return AddEmail(data, token, client_ip).execute()

@emails_blueprint.route('/emails/ping', methods = ['GET'])
def ping():
    return 'pong', 200