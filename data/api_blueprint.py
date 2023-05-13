from flask import Blueprint

blueprint = Blueprint(
    'inv_api',
    __name__,
    template_folder='templates'
)

from . import objects_api
from . import history_api
from . import places_api
from . import qr_api
from . import login_api
from . import users_api
