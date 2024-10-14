from flask import request, Blueprint
import os
from flask.json import jsonify
from commands.get import GetEmail
from commands.add import AddEmail
from errors.errors import ApiError, NotToken, TokenInvalid
from models.models import Email

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

@emails_blueprint.route('/emails/<string:email>', methods = ['GET'])
def read(email):
    authorization_token = request.headers.get('Authorization')
    token = None
    if authorization_token is not None:
        token = authorization_token.replace('Bearer ', '')
    else:
        raise NotToken
    
    GetEmail(email, token).execute()
 