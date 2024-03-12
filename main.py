from flask import Flask
from src.blueprint.HexBlueprint import hex_route

app = Flask(__name__)
app.register_blueprint(hex_route)

