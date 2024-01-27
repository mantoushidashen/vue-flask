from flask_httpauth import HTTPTokenAuth
from common.config import secret_key
from flask import g, make_response, jsonify,request
from authlib.jose import jwt, JoseError
from authlib.jose.errors import ExpiredTokenError, BadSignatureError, DecodeError
from model.User import User
from common.response_code import ResponseCode

auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token):
    g.token_error = False
    g.token_timeout = False
    try:
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]  # 从头部获取令牌部分
                if isinstance(token, bytes):
                    token = token.decode('utf-8')
                token = token.replace("b'", "").replace("'", "")
        data = jwt.decode(token, secret_key)
        g.current_user = User.query.get(data['id'])
    except JoseError:
        g.token_error = True
        return False
    except ExpiredTokenError:
        g.token_timeout = True
        return False
    except (BadSignatureError, DecodeError):
        g.token_error = True
        return False
    except JoseError as e:
        # 处理其他类型的Jose错误
        print(f"JWT解码错误：{e}")
        g.token_error = True
        return False
    return True

@auth.error_handler
def unauthorized():
    if g.token_error:
        return ResponseCode.response(
            success=False,
            code=ResponseCode.TOKEN_ERROR,
            message='Token Error'
        )
    if g.token_timeout:
        return ResponseCode.response(
            success=False,
            code=ResponseCode.TOKEN_EXPIRED,
            message='Token Expired'
        )
    return ResponseCode.response(
        success=False,
        code=ResponseCode.UNAUTHORIZED,
        message='Unauthorized'
    )