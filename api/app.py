from logging import getLogger
from flask_sock import Sock # type: ignore
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api # type: ignore

from api.bridge_blueprint import bridge_data_blueprint
from server_thread import ServerThread

logger = getLogger(__name__)

class APIServer:
    """API server class."""

    def __init__(
        self,
        host: str = '0.0.0.0',
        port: int = 8000
    ):
        # GUI settings
        self.host: str = host
        self.port: int = port
        self.app = Flask(__name__, template_folder='templates', static_folder='static')
        CORS(self.app)
        self.sock = Sock(self.app) # type: ignore
        self.app.config["API_TITLE"] = "irmos API"
        self.app.config["API_VERSION"] = "1.0"
        self.app.config["OPENAPI_VERSION"] = "3.0.2"
        self.app.config["OPENAPI_URL_PREFIX"] = "/"
        self.app.config["OPENAPI_JSON_PATH"] = "irmos-openapi.json"  # Path to OpenAPI JSON
        self.app.config["OPENAPI_SWAGGER_UI_PATH"] = "/api"
        self.app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  # Swagger UI

        self.api = Api(self.app)
        self.api.register_blueprint(bridge_data_blueprint) # type: ignore

        self.server: ServerThread = ServerThread(self.app, self.host, self.port)


    def start(self) -> None:
        """Create and start a new thread for the API server."""
        self.server.start()
        logger.debug('Start API server at %s:%s', self.host, str(self.port))

if __name__ == "__main__":
    api_server = APIServer()
    api_server.start()