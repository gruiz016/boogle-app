from boggle import Boggle
from flask import Flask, redirect, request, render_template, session, jsonify, flash

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc1234'

words = set()


@app.route('/')
def index():
    '''Renders the game board and starts a session on the client browser to take the progress throughout the game'''
    board = boggle_game.make_board()
    session['high-score'] = session.get('high-score')
    session['times-played'] = session.get('times-played', 0) + 1
    session['board'] = board
    return render_template('index.html', board=board)


@app.route('/check-word')
def get_result():
    '''Checks the response from the client and determines if the word is correct and sends the response to the client.'''
    word = request.args['word']
    board = session['board']
    result = check_word(board, word)
    return jsonify({"result": result})


@app.route('/end-game', methods=['POST'])
def set_results():
    '''Recieves the high-score from the client and stores it in client memory.'''
    score = request.json['high-score']
    if score > session['high-score']:
        session['high-score'] = score
    return jsonify({'high-score': session['high-score']})


def check_word(board, word):
    '''Checks to see weather the word has been sent previously.'''
    if word not in words:
        words.add(word)
        return boggle_game.check_valid_word(board, word)
    else:
        return 'already added'
