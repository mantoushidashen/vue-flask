from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from views import upload,login

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(upload.blueprint)
app.register_blueprint(login.blueprint)
 

  
if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)