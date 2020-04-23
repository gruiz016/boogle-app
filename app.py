from boggle import Boggle
from flask import Flask, redirect, request, render_template, session, jsonify, flash

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc1234'

words = set()


@app.route('/')
def index():
    board = boggle_game.make_board()
    session['high-score'] = session.get('high-score')
    session['times-played'] = session.get('times-played', 0) + 1
    session['board'] = board
    return render_template('index.html', board=board)


@app.route('/check-word')
def get_result():
    word = request.args['word']
    board = session['board']
    result = check_word(board, word)
    return jsonify({"result": result})


@app.route('/end-game', methods=['POST'])
def set_results():
    score = request.json
    if score['high-score'] > session['high-score']:
        session['high-score'] = score['high-score']
    return request.json


def check_word(board, word):
    if word not in words:
        words.add(word)
        return boggle_game.check_valid_word(board, word)
    else:
        return 'already added'
