from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from src.models.models import db
import os
from src.errors.errors import ApiError
from src.blueprints.emails import emails_blueprint

loaded = load_dotenv('.env.development')

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME =  os.environ["DB_NAME"]
APP_PORT =  int(os.getenv("APP_PORT", default=3000))

application = Flask(__name__)
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