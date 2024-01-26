from flask_httpauth import HTTPTokenAuth
from config import secret_key
from flask import g, make_response, jsonify,request
from authlib.jose import jwt, JoseError
from authlib.jose.errors import ExpiredTokenError, BadSignatureError, DecodeError

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
        print(data)
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
        return make_response(jsonify({'code':402,'error': 'Token Error'}), 402)

    if g.token_timeout:
        return make_response(jsonify({'code':401,'error': 'Token Expired'}), 401)