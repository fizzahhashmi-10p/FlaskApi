from flask import Blueprint, render_template, abort
#from jinja2 import TemplateNotFound
from models import Tasks
from flask_restful import marshal_with
from routes import task_fields

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')
simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')

@api_bp.route('/task')
@api_bp.route('/task/<id>')
@marshal_with(task_fields)
def getdata(id=None):
    task = Tasks.query.filter_by(id=id).first()
    print(task)
    return task


    

@simple_page.errorhandler(404)
@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template(f'{page}.html')
    except:
        return {"erorr":"pages/404.html"}

