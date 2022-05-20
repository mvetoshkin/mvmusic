from flask import Blueprint

from .views.index import index_view

bp = Blueprint('general', __name__, url_prefix='/')
bp.add_url_rule('/', view_func=index_view)
