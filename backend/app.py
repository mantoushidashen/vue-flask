import common.db_config as db_config
from common.db_config import db
from flask import Flask, request
from flask_cors import CORS
from views import upload,login,novel
from model.User import User

app = Flask(__name__)
app.config.from_object(db_config)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(upload.blueprint)
app.register_blueprint(login.blueprint)
app.register_blueprint(novel.blueprint)

def create_tables():
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()    

if __name__ == '__main__':
    create_tables()
    app.run(host = '0.0.0.0', debug=True)