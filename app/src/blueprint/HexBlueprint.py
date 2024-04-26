from flask import Blueprint, render_template, session, request
import jsonpickle

from src.entity.Cell import Cell
from src.service.HexService import (createGame, createHeuristicTree, applyMinimax,
                                    applyNegamax, applyAlphaBeta, applyNegAlphaBeta, applySSS)

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
    game = createGame(4, 1)
    heuristictree = createHeuristicTree(game.board, 4)
    applySSS(heuristictree)
    return render_template('game/gamePage.html.jinja', game=game, heuristictree=heuristictree)


@hex_route.route('/hex/game/create/game/parameters')
def createGameParameters():
    return render_template('game/gamePage.html.jinja')


@hex_route.route('/hex/game/parameters')
def selectGameParameters():
    game = createGame(int(request.args['board-size']), int(request.args['difficulty']))
    session['game'] = jsonpickle.encode(game)
    return render_template('game/gameBoard.html.jinja', game=game)


@hex_route.route('/hex/game/play')
def playOnce(cell: Cell):
    game = jsonpickle.decode(session['game'])
    heuristictree = createHeuristicTree(game.board, game.difficultyLevel)
    return render_template('game/gameBoard.html.jinja', game=game)


@hex_route.route('/hex/documentation/history')
def displayHexHistory():
    return render_template('documentation/displayHistory.html.jinja')
