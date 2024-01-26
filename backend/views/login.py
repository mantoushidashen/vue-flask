
from flask import Blueprint,request
from flask_restful import reqparse, Resource, Api
from config import admin_passwd, secret_key
from utils.token_auth import auth
from authlib.jose import jwt

blueprint = Blueprint('login',__name__)
api = Api(blueprint)

parser = reqparse.RequestParser()
parser.add_argument('username',type=str)
parser.add_argument('password',type=str)

class User(Resource):
    def create_token(self, user_id, **kwargs):
        header = {'alg': 'HS256'}
        data = {'id': user_id}
        data.update(**kwargs)
        token = jwt.encode(header=header, payload=data, key=secret_key)
        return token

    @auth.login_required
    def get(self, user_opt):
        if user_opt == 'info':
            return {
            "code": 20000,
            "data": {"roles": ["admin"],"name": "admin","avatar": "s1.gif"}}
        
    #  生成token
    def post(self, user_opt):
        if user_opt == 'login':
            args = parser.parse_args()
            username = args.get('username')
            password = args.get('password')
            if password == admin_passwd and username == "admin":
                token = self.create_token(admin_passwd)
                return {"code": 20000,"data": {"token": "Bearer {}".format(token)}}
            else:
                return {"code": 40000, "data": "密码错误！"}
        elif user_opt == 'logout':
            return {"code": 20000,"data": "success"}

api.add_resource(User, '/api/user/<user_opt>')