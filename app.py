from flask import Flask, render_template, request, jsonify, session
from boggle import Boggle
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretKey"

boggle_game = Boggle()


def dir_last_updated(folder):
    """This function allows the flask app and chrome browser work
    so that my most recently saved file is used by the running server"""
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                    for root_path, dirs, files in os.walk(folder)
                    for f in files))

@app.route('/')
def start_page():
    """Display the home/start page of the survey app"""

    game_board = boggle_game.make_board()
    session['g_board'] = game_board
    highscore = session.get("highscore", 0)
    n_plays = session.get("n_plays", 0)

    return render_template("board.html",
                            last_updated=dir_last_updated('/home/jw/Programs/SpringBoard/flask-boggle/static'),
                            board=game_board,
                            highscore=highscore,
                            n_plays=n_plays)

@app.route('/check-word')
def check_word():
    """Check a guessed word for validity"""
    word = request.args["word"]
    board = session["g_board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """At the appropriate time post the score for the current game"""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    n_plays = session.get("n_plays", 0)

    session['n_plays'] = n_plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord = score > highscore)