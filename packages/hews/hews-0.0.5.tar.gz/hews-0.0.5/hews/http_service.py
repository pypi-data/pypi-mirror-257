from hews.core import x
from flask import Flask

app = Flask(__name__)


@app.route('/')
def root():
    from hews.initialize.root.projects.default.applications.default.modules.default.index import index
    ind = index(x.jun_project_core('default').jun_application_core('default').jun_module_core('default'))
    return ind.http()
