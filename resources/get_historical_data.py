from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from .mt_methods import get_historical_data

blp = Blueprint("get_historical_data",__name__,description="Raw data")

@blp.route("/get_historical_data")
class Copy_rates_from_pos(MethodView):
    def post(self):
        payload = request.get_json()
    
        if(
            "symbol" not in payload or
            "timeframe" not in payload or
            "start_pos" not in payload or
            "count" not in payload 
        ):
            abort(
                400,
                message="Bad request."
            )
        try:
            return get_historical_data(
                payload['symbol'],
                payload['timeframe'],
                payload['start_pos'],
                payload['count'],)
        except Exception as e:
            abort(500,message="ERROR! : "+e)