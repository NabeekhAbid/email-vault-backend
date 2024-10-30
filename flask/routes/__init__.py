from flask import Blueprint, Flask, jsonify

from common.dto import ResponseDTO
from common.utils.constants import BASE_URL_PREFIX

from .user_routes import user_bp

test = Blueprint('api', __name__)

@test.route('/test', method=['GET'])
def test_route():
    Response_dto = ResponseDTO(data=None, message="server is running!", status=200)
    return jsonify(Response_dto.to_dict()), Response_dto.status

def register_routes(app: Flask):
    app.register_blueprint(test)
    app.register_blueprint(user_bp, url_prefix=BASE_URL_PREFIX)