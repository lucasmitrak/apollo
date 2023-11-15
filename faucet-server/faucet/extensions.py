from flask_cache import Cache
from flask_login import LoginManager
from flask_restful import Api

from faucet.models import User

# Setup flask cache
cache = Cache()

rest_api = Api(prefix="/api/v1/")

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
