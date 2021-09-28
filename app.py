from flask import Flask
from flask_restful import Api


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG'] = True


api = Api(app)
from routes import Todo
api.add_resource(Todo, '/api/todo/')

from bp_routes import api_bp, simple_page 
app.register_blueprint(api_bp)
app.register_blueprint(simple_page)
#print(app.url_map)


if __name__ == '__main__':
    app.run(debug=True)
