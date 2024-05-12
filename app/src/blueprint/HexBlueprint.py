from flask import Blueprint, render_template, session, request, redirect
import jsonpickle

from src.service.HexService import *
from src.service.WinnerVerification import *

hex_route = Blueprint('hex_route', __name__, template_folder='templates')


@hex_route.route('/')
def show():
    return render_template('index.html.jinja')

@hex_route.route('/hex/game')
def showGame():
    game = jsonpickle.decode(session['game'])
    winner = getWinner(game.board)
    if winner is not Status.NONE:
        game.setWinner(winner)
        game.setIsGameFinished(True)
    return render_template('game/gameBoard.html.jinja', game=game, winner=winner.value)

@hex_route.route('/hex/game/create/game/parameters')
def createGameParameters():
    return render_template('game/gamePage.html.jinja')


@hex_route.route('/hex/game/parameters')
def selectGameParameters():
    session['game'] = None
    game = createGame(int(request.args['board-size']), int(request.args['difficulty']),
                      int(request.args['heuristic']) ,int(request.args['algorithm']))
    session['game'] = jsonpickle.encode(game)
    return redirect('/hex/game', code=302)


@hex_route.route('/hex/game/play/<x>/<y>')
def playOnce(x: int, y: int):
    game = jsonpickle.decode(session['game'])
    cell = game.board.getCell(int(x), int(y))
    playOneMove(cell, game)
    session['game'] = jsonpickle.encode(game)
    return redirect('/hex/game', code=302)

@hex_route.route('/hex/documentation/history')
def displayHexHistory():
    return render_template('documentation/displayHistory.html.jinja')

@hex_route.route('/hex/documentation/examples')
def displayHexExamples():
    return render_template('documentation/examples.html.jinja')
