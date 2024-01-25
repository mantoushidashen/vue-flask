from flask import request
from flask import Blueprint
from flask_restful import reqparse, Resource, Api
from config import admin_passwd, secret_key
from utils.token_auth import auth
from itsdangerous import URLSafeTimedSerializer as Serializer

s = Serializer(secret_key)

blueprint = Blueprint('login',__name__)
api = Api(blueprint)

parser = reqparse.RequestParser()
parser.add_argument('username',type=str)
parser.add_argument('password',type=str)

class User(Resource):
    # @auth.login_required
    def get(self, user_opt):
        if user_opt == 'info':
            return {
                    "code": 20000,
                    "data": {"roles": ["admin"],"name": "admin","avatar": "/s1.gif"}}
    #  生成token
    def post(self, user_opt):
        if user_opt == 'login':
            args = parser.parse_args()
            username = args.get('username')
            password = args.get('password')
            if password == admin_passwd and username == "admin":
                token = s.dumps(admin_passwd)
                return {"code": 20000, "data": {"token": token}}
            else:
                return {"code": 40000, "data": "密码错误！"}
        elif user_opt == 'logout':
            return {"code": 20000, "data": "success"}

api.add_resource(User, '/api/user/<user_opt>')