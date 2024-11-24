from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src import routes
from src.common.constants import JWT_ACCESS_TOKEN_EXPIRES
from src.common.constants import JWT_REFRESH_TOKEN_EXPIRES
from src.common.constants import JWT_SECRET_KEY


def create_app(flask_app=None):
    flask_app = flask_app or Flask(__name__)
    flask_app.register_blueprint(routes.blueprint)
    Swagger(flask_app)
    CORS(flask_app)
    flask_app.config["DEBUG"] = True
    flask_app.config["PROPAGATE_EXCEPTIONS"] = True
    flask_app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
    flask_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = JWT_REFRESH_TOKEN_EXPIRES
    flask_app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    JWTManager(flask_app)
    return flask_app


app = Flask(__name__)
create_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
