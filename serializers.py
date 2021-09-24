from flask_restful import reqparse
from flask_restful.fields import DateTime

def getArgParser():
    # Define parser and request args
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('title', type=str)
    parser.add_argument('completion_status', type=bool)
    parser.add_argument('updatedOn', type=DateTime)

    return parser