from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from .mt_methods import copy_rates_from_pos

blp = Blueprint("copy_rates_from_pos",__name__,description="Raw data")

@blp.route("/copy_rates_from_pos")
class Copy_rates_from_pos(MethodView):
    def post(self):
        payload = request.get_json()
    
        if(
            "symbol" not in payload or
            "timeframe" not in payload or
            "start_pos" not in payload or
            "count" not in payload or
            "multiplier" not in payload or
            "threshold" not in payload or
            "closeOnly" not in payload
        ):
            abort(
                400,
                message="Bad request."
            )
        try:
            
            return copy_rates_from_pos(
                payload['symbol'],
                payload['timeframe'],
                payload['start_pos'],
                payload['count'],
                payload['multiplier'],
                payload['threshold'],
                payload['closeOnly'])
        except Exception as e:
            abort(500,message="ERROR! : "+e)
