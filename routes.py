from datetime import datetime
from flask import request
from flask_restful import Resource, fields, marshal_with
from serializers import getArgParser
from models import db, Tasks
from werkzeug.exceptions import BadRequest

parser = getArgParser()


task_fields = {
    'id':fields.Integer,
    'title':fields.String,
    'createdOn':fields.DateTime,
    'completion_status':fields.Boolean,
    'updatedOn':fields.DateTime
}


class Todo(Resource):
    @marshal_with(task_fields)
    def get(self):
        args = request.args
        if args:
            task = Tasks.query.filter_by(id=args['id']).first()
            return task
        else:
            tasks = Tasks.query.all()
            return tasks

    def post(self):
        try:
            args = parser.parse_args()
            task = Tasks(id = args['id'], title = args['title'], completion_status = args['completion_status'])
            db.session.add(task)
            db.session.commit()
            return {"id": args['id'], "post request status": "successful", "code":201}
        except:
            raise BadRequest('Task Already Exists!')
            

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
            raise BadRequest('Unable to update task')

    def patch(self):
        args = request.args
        if Tasks.query.filter_by(id=args['id']).first():
            args = parser.parse_args()
            args["updatedOn"]= datetime.now()
            Tasks.query.filter_by(id=args['id']).update(args)
            db.session.commit()
            return {"id": args['id'], "patch request status": "successful", "code":200}
        else:
            raise BadRequest('Unable to update task')
    
    def delete(self):
        args = request.args
        task = Tasks.query.filter_by(id=args['id']).first()
        if task:
            print(task)
            db.session.delete(task)
            db.session.commit()
            return {"id": args['id'], "delete request status": "successful", "code":204}
        else:
            raise BadRequest('Task doesnot exist!')



