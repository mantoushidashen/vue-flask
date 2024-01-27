
from flask import Blueprint,request,g
from flask_restful import reqparse, Resource, Api
from common.config import secret_key
from utils.token_auth import auth
from authlib.jose import jwt
from datetime import datetime, timedelta
from model.User import User
from common.response_code import ResponseCode

blueprint = Blueprint('login',__name__)
api = Api(blueprint)

parser = reqparse.RequestParser()
parser.add_argument('username',type=str)
parser.add_argument('password',type=str)

class UserApi(Resource):
    def __init__(self):
        pass

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
            if g.current_user:
                user_info = {
                    "roles": g.current_user.roles,
                    "name": g.current_user.username,
                    "avatar": g.current_user.avatar
                }
                return ResponseCode.response(success=True, code=ResponseCode.SUCCESS, data=user_info)
            else:
                return ResponseCode.response(success=False, code=ResponseCode.USER_NOT_FOUND, message="用户不存在!")
        
    #  生成token
    def post(self, user_opt):
        if user_opt == 'login':
            args = parser.parse_args()
            username = args.get('username')
            password = args.get('password')
            result = self.query_record(username)
            if result is None:
                return ResponseCode.response(success=False, code=ResponseCode.USER_NOT_FOUND, message="用户不存在！")
            if result['password'] == password:
                token = self.create_token(result['id'])
                return ResponseCode.response(success=True, code=ResponseCode.SUCCESS, data={"token": "Bearer {}".format(token)})
            else:
                return ResponseCode.response(success=False, code=ResponseCode.USER_NOT_FOUND, message="密码错误！")
        elif user_opt == 'logout':
            return ResponseCode.response(success=True, code=ResponseCode.SUCCESS, data="success")
        elif user_opt == 'register':
            args = parser.parse_args()
            if args.get('username') and args.get('password'):
                User(username=args.get('username'), password=args.get('password')).save()
            return ResponseCode.response(success=True, code=ResponseCode.SUCCESS, data="success")


api.add_resource(UserApi, '/api/user/<user_opt>')