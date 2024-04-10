from flask import Blueprint, render_template, session, request

from src.service.HexService import createGame, createHeuristicTree, applyMinimax, applyNegamax, applyAlphaBeta

hex_route = Blueprint('hex_route', __name__, template_folder='templates')

@hex_route.route('/')
def show():
    return render_template('index.html.jinja')


@hex_route.route('/hex/game/create/game/example')
def createExample():
    game = createGame(4, 1)
    heuristictree = createHeuristicTree(game.board, 4)
    applyMinimax(heuristictree)
    game = createGame(16, 1)
    heuristictree = createHeuristicTree(game.board, 16)
    applyNegamax(heuristictree)
    game = createGame(4, 1)
    heuristictree = createHeuristicTree(game.board, 4)
    applyAlphaBeta(heuristictree)
    return render_template('game/gamePage.html.jinja', game=game, heuristictree=heuristictree)

@hex_route.route('/hex/game/create/game/parameters')
def createGameParameters():
    return render_template('game/gamePage.html.jinja')

@hex_route.route('/hex/game/parameters')
def selectGameParameters():
    game = createGame(int(request.args['board-size']), int(request.args['difficulty']))
    heuristictree = createHeuristicTree(game.board, 1) #TODO height
    session['board-size'] = request.args['board-size']
    session['difficulty'] = request.args['difficulty']
    return render_template('game/gameBoard.html.jinja')
