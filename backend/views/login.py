
from flask import Blueprint,request,g
from flask_restful import reqparse, Resource, Api
from common.config import admin_passwd, secret_key
from utils.token_auth import auth
from authlib.jose import jwt
from datetime import datetime, timedelta
from model.User import User

blueprint = Blueprint('login',__name__)
api = Api(blueprint)

parser = reqparse.RequestParser()
parser.add_argument('username',type=str)
parser.add_argument('password',type=str)

class UserApi(Resource):
    def __init__(self):
        self.role_msg = {}

    def query_record(self, username):
        result = User.query.filter_by(username=username).first()
        if result:
            role_msg = {"id":result.id, "roles":result.roles, "name": result.username,"password": result.password,"avatar": result.avatar}
            return role_msg
        else:
            return None
    
    def create_token(self, user_id, **kwargs):
        header = {'alg': 'HS256'}
        data = {'id': user_id}
        data.update(**kwargs)
        expire_time = datetime.utcnow() + timedelta(microseconds=10)
        data['exp'] = expire_time
        token = jwt.encode(header=header, payload=data, key=secret_key)
        return token

    @auth.login_required
    def get(self, user_opt):
        if user_opt == 'info':
            user_info = {
                "roles": g.current_user.roles,
                "name": g.current_user.username,
                "avatar": g.current_user.avatar
            }
            return {
                "code": 20000,
                "data": user_info
            }
        
    #  生成token
    def post(self, user_opt):
        if user_opt == 'login':
            args = parser.parse_args()
            username = args.get('username')
            password = args.get('password')
            result = self.query_record(username)
            if result['password'] == password:
                token = self.create_token(result['id'])
                return {"code": 20000,"data": {"token": "Bearer {}".format(token)}}
            else:
                return {"code": 40000, "data": "密码错误！"}
        elif user_opt == 'logout':
            return {"code": 20000,"data": "success"}
        elif user_opt == 'register':
            args = parser.parse_args()
            if args.get('username') and args.get('password'):
                User(username=args.get('username'), password=args.get('password')).save()
            return {"code": 20000,"data": "success"}


api.add_resource(UserApi, '/api/user/<user_opt>')