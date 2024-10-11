from flask import request, Blueprint
import os
from flask.json import jsonify

emails_blueprint = Blueprint('emails', __name__)

@emails_blueprint.route('/blacklists', methods=['POST'])
def create():
    pass

@emails_blueprint.route('/emails/ping', methods = ['GET'])
def ping():
    return 'pong', 200