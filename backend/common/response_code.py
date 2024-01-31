#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import jsonify

class ResponseCode:
    SUCCESS = 20000
    UNAUTHORIZED = 40100
    TOKEN_ERROR = 40200
    TOKEN_EXPIRED = 40300
    PASSWORD_ERROR = 40000
    USER_NOT_FOUND = 40400
    SERVER_ERROR = 50000

    @staticmethod
    def response(success=True, code=SUCCESS, data=None, message=None):
        # 只返回可以被序列化为 JSON 的数据结构
        return {
            "success": success,
            "code": code,
            "data": data,
            "message": message
        }
