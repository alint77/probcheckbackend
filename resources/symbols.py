from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from .mt_methods import getAllSymbolNames,copy_rates_from_pos

blp = Blueprint("symbols",__name__,description="Symbols")

@blp.route("/symbols")
class Symbols(MethodView):
    def get(self):
        
        try:
            return getAllSymbolNames()
        except:
            abort(500,message="Something went wrong")