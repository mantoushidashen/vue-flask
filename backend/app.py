import db_config
from db_config import db
from flask import Flask
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
    user1 = User(username='admin', password='123456')
    db.session.add(user1)
    # 需要提交事务给数据库
    db.session.commit()
    return 'add success!'

# 查找数据的路由
@app.route('/query')
def query_record():
    # 查找id=1的第一个对象
    result = User.query.get(1)
    print(result.username, result.password)
    return f'query success!{result.username, result.password}'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)