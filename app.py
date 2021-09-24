from datetime import datetime
from flask import Flask, request
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from serializers import getArgParser

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
from models import db, Tasks
parser = getArgParser()

task_fields = {
    'id':fields.Integer,
    'title':fields.String,
    'createdOn':fields.DateTime,
    'completion_status':fields.Boolean,
    'updatedOn':fields.DateTime
}

from models import Tasks
class Todo(Resource):
    @marshal_with(task_fields)
    def get(self):
        args = request.args
        if args:
            task = Tasks.query.filter_by(id=args['id']).first()
            print(task)
            return task
        else:
            tasks = Tasks.query.all()
            return tasks

    def post(self):
        try:
            #args = request.data
            args = parser.parse_args()
            task = Tasks(id = args['id'], title = args['title'], completion_status = args['completion_status'])
            db.session.add(task)
            db.session.commit()
            #print()
            return {"id": args['id'], "post request status": "successful", "code":201}
        except:
            return {"id": args['id'], "post request status": "failed", }

    def put(self):
        args = request.args
        task = Tasks.query.filter_by(id=args['id'])
        if task:
            args = parser.parse_args()
            args["updatedOn"]= datetime.now()
            task.update(args)
            db.session.commit()
            return {"id": args['id'], "put request status": "successful", "code": 205}
        else:
            return {"id": args['id'], "put request status": "failed"}

    def patch(self):
        args = request.args
        task = Tasks.query.filter_by(id=args['id'])
        if task:
            args = parser.parse_args()
            args["updatedOn"]= datetime.now()
            task.update(args)
            db.session.commit()
            return {"id": args['id'], "patch request status": "successful", "code":200}
        else:
            return {"id": args['id'], "patch request status": "failed"}
    
    def delete(self):
        try:
            args = request.args
            get_todo = Tasks.query.get(args['id'])
            db.session.delete(get_todo)
            db.session.commit()
            return {"id": args['id'], "delete request status": "successful", "code":204}
        except:
            return {"id": args['id'], "delete request status": "failed"}


api.add_resource(Todo, '/api/todo/')

if __name__ == '__main__':
    app.run(debug=True)