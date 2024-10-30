from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from blacklist.src.models.models import db
import os
from blacklist.src.errors.errors import ApiError
from blacklist.src.blueprints.emails import emails_blueprint

# Cargar variables de entorno
loaded = load_dotenv('.env.development')

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
APP_PORT = int(os.getenv("APP_PORT", default=3000))

application = Flask(__name__)

# Configuración condicional de la base de datos
if os.getenv('FLASK_ENV') == 'testing':
    application.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
else:
    application.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config["PROPAGATE_EXCEPTIONS"] = True
application.register_blueprint(emails_blueprint)

app_context = application.app_context()
app_context.push()
cors = CORS(application)
db.init_app(application)
db.create_all()
api = Api(application)

@application.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "message": err.description
    }
    return jsonify(response), err.code

if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0", port=APP_PORT)