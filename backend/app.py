import common.db_config as db_config
from common.db_config import db
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from views import upload,login,novel
from model.User import User

app = Flask(__name__)
app.config.from_object(db_config)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(upload.blueprint)
app.register_blueprint(login.blueprint)
app.register_blueprint(novel.blueprint)

with app.app_context():
    db.app = app
    db.init_app(app)
    db.create_all()     # 在应用上下文中创建所有表

# 添加数据的路由
@app.route('/add')
def add_record():
    user1 = User(roles='admin', username='admin', password='123456', avatar= "s1.gif")
    db.session.add(user1)
    # 需要提交事务给数据库
    db.session.commit()
    return 'add success!'

# 查找数据的路由
@app.route('/query')
def query_record():
    # 从请求参数中获取username
    username = request.args.get('name')
    if not username:
        return 'Please provide a username.', 400  # 如果没有提供用户名，则返回错误
    result = User.query.filter_by(username=username).first()
    if result:
        print(result.username, result.password)
        return f'User found! Username: {result.username}, Password: {result.password}'
    else:
        return 'User not found.', 404

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)