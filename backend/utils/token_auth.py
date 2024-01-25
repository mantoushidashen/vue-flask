from flask import request
from itsdangerous import URLSafeTimedSerializer as Serializer
from config import secret_key
from flask_httpauth import HTTPTokenAuth

s = Serializer(secret_key)
auth = HTTPTokenAuth()

# 认证客户端传递过来的token是否正确
@auth.verify_token
def verify_token(token):
    if token is None:
        token = request.headers.get('Authorization')
    try:
        print(f"Token after removing Bearer: {token}")
        data = s.loads(token, max_age=28800)
    except Exception as e:
        print("Some other exception in token verification", e, flush=True)
        return False
    return data

# 错误处理器
@auth.error_handler
def unauthorized():
    return {"code": 50000, "data": "403：认证异常，请重新登录！"}, 200