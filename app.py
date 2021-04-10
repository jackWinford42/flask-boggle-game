from flask import Flask, render_template, request, jsonify, session
from boggle import Boggle
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "VerySecret"

boggle = Boggle()

@app.route("/")
def home():
    """Display the home page of the survey app
    with full game interface"""

    #initial one time setup of essential variables
    session["board"] = boggle.make_board()
    session["highscore"] = 0
    session["timesPlayed"] = 0

    return render_template("board.html",
                            board=session["board"],
                            highscore=session["highscore"],
                            timesPlayed=session["timesPlayed"])

@app.route("/verify-guess")
def verify():
    """Check a guessed word for validity"""
    guess = request.args["word"]

    validity = boggle.check_valid_word(session["board"], guess)

    return jsonify({'result': validity})

@app.route("/score-game", methods=["POST"])
def score():
    """At the appropriate time, score the current game"""

    score = request.json["score"]
    times_played = session.get("timesPlayed", 0)

    session["timesPlayed"] = times_played + 1

    #set highscore to the max between current score and the highscore
    session["highscore"] = max(score, session.get("highscore", 0))

    return jsonify(brokeRecord = score > session["highscore"])