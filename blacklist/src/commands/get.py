from models.models import db, Email
from commands.base_command import BaseCommannd
from sqlalchemy.exc import SQLAlchemyError
import hashlib
import uuid
from flask import jsonify
from datetime import datetime
import pytz
from requests import Response
import os
from errors.errors import ApiError, NotToken, TokenInvalid, NotFound, BadRequest, EmailExist

class GetEmail(BaseCommannd):
    def __init__(self, email, token):
        self.email = email
        self.token = token
        self.real_token = os.getenv("TOKEN")        
    
    def execute(self):
        if self.token != self.real_token:
            raise TokenInvalid
        
        if not self.email:
            raise NotFound
        
        if not isinstance(self.email, str):
            raise BadRequest

        email_bd = Email.query.filter(Email.email == self.email).first()
   
        if email_bd is None:
            return jsonify({
            "exist": False,
            }), 200
        
        else:    
            return jsonify({
            "exist": True,
            "reason": email_bd.reason
            }), 200            





