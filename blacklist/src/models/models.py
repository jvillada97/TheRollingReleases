from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    app_id = db.Column(UUID(as_uuid=True), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(255), nullable=True)
    creation_date = db.Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "reason": self.reason,
            "ip_address": self.ip_address,
            "creation_date": self.creation_date
        }

class EmailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Email
        id = fields.String()