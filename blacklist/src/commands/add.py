from blacklist.src.models.models import db, Email
from blacklist.src.commands.base_command import BaseCommannd
from flask import jsonify
from datetime import datetime
import pytz
import os
from blacklist.src.errors.errors import ApiError, NotToken, TokenInvalid, NotFound, BadRequest, EmailExist

class AddEmail(BaseCommannd):
    def __init__(self, data, token, client_ip):
        self.data = data
        self.token = token
        self.real_token = os.getenv("TOKEN")
        self.client_ip = client_ip
    
    def execute(self):
        if self.token != self.real_token:
            raise TokenInvalid
        
        if not self.data or 'email' not in self.data or "app_uuid" not in self.data or "blocked_reason" not in self.data:
            raise NotFound
        
        if not isinstance(self.data['email'], str) or not isinstance(self.data['app_uuid'], str) or not isinstance(self.data['blocked_reason'], str):
            raise BadRequest

        check_email = Email.query.filter_by(email=self.data['email']).first()

        if check_email is not None: 
            raise EmailExist

        new_email = Email(
            app_id=self.data['app_uuid'],
            email=self.data['email'],
            reason=self.data['blocked_reason'],
            ip_address=self.client_ip,
            creation_date=datetime.utcnow().replace(tzinfo=pytz.UTC)
        )

        db.session.add(new_email)
        db.session.commit()
        return jsonify({
            "msg": f"El email {self.data['email']} ha sido añadido correctamente a la blacklist"
        }), 201





