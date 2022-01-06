import importlib
import os

from flask import Blueprint

from mvmusic.libs import to_camel_case
from . import views
from .views import BaseView

bp = Blueprint('subsonic_api', __name__, url_prefix='/rest')

for file in os.listdir(os.path.dirname(views.__file__)):
    if not file.startswith('__') and file.endswith('.py'):
        view_name = file.rpartition('.')[0]
        module = importlib.import_module(f'{views.__package__}.{view_name}')
        for obj_name in dir(module):
            if not obj_name.endswith('View'):
                continue

            obj = getattr(module, obj_name)
            if obj != BaseView and issubclass(obj, BaseView):
                path = to_camel_case(view_name)
                as_view = getattr(obj, 'as_view')
                view_func = as_view(view_name + '_view')
                bp.add_url_rule(f'/{path}', view_func=view_func)
                bp.add_url_rule(f'/{path}.view', view_func=view_func)
