from flask import Blueprint, request, jsonify
from models.user import search_username

search_user = Blueprint('search_user', __name__, url_prefix='/search_user')


@search_user.route('/', methods=['POST'])
def search_for_user():
    if request.is_json:
        request_json = request.get_json()
        if 'query' in request_json:
            users = search_username(request_json['query'])
            result = []
            for user in users:
                result.append(user.username)
            return jsonify({'users': result})
    return '', 400
