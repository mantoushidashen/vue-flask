#!/usr/bin/python3
# -*- coding: utf-8 -*-

from common.db_config import db  # 导入db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    roles = db.Column(db.String(50),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    avatar = db.Column(db.String(100),nullable=False)

