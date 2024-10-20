from flask import request, Blueprint
import os
from flask.json import jsonify
from src.commands.get import GetEmail
from src.commands.add import AddEmail
from src.errors.errors import ApiError, NotToken, TokenInvalid
from src.models.models import Email

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

@emails_blueprint.route('/blacklists/ping', methods = ['GET'])
def ping():
    return 'pong', 200

@emails_blueprint.route('/blacklists/<string:email>', methods = ['GET'])
def read(email):
    authorization_token = request.headers.get('Authorization')
    token = None
    if authorization_token is not None:
        token = authorization_token.replace('Bearer ', '')
    else:
        raise NotToken
    
    return GetEmail(email, token).execute()
 