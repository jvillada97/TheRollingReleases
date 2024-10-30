from flask import request, Blueprint
from blacklist.src.commands.get import GetEmail
from blacklist.src.commands.add import AddEmail
from blacklist.src.errors.errors import ApiError, NotToken, TokenInvalid

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
    
    #return GetEmail(email, token).execute()
 