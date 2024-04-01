from flask import Blueprint, render_template

from src.service.HexService import createGame, createHeuristicTree

hex_route = Blueprint('hex_route', __name__, template_folder='templates')
@hex_route.route('/')
def show():
    return render_template('index.html.jinja')

@hex_route.route('/hex/game/parameters')
def selectGameParametersGame():
    game = createGame(4, 1)
    heuristictree = createHeuristicTree(game.board, 4)
    return render_template('game/gamePage.html.jinja', game=game, heuristictree=heuristictree)