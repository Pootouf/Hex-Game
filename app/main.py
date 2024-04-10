from flask import Flask
from src.blueprint.HexBlueprint import hex_route

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc'
app.register_blueprint(hex_route)

