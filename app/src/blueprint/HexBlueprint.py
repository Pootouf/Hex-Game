from flask import Blueprint, render_template

hex_route = Blueprint('hex_route', __name__, template_folder='templates')
@hex_route.route('/')
def show():
    return render_template('index.html.jinja')