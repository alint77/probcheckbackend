from flask import Flask
from flask_smorest import Api
from resources.raw_data_endpoints import blp as RawDataBlp 
from resources.symbols import blp as SymbolsBlp 

app=Flask(__name__)

app.config["PROPOGATE_EXCEPTIONS"]=True
app.config["API_TITLE"]="Market CandleByCandle ProbCalc API"
app.config["API_VERSION"]="0.1"
app.config["OPENAPI_VERSION"]="3.0.3"
app.config["OPENAPI_URL_PREFIX"]="/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(RawDataBlp)
api.register_blueprint(SymbolsBlp)

