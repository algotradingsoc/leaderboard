from flask import Flask, render_template

from config import CHALLENGES
from rank_order import rank_order

app = Flask(__name__)


@app.route("/")
def leader_board():
    top_50_teams = rank_order()
    print(CHALLENGES)
    return render_template("index.html", len=len(top_50_teams), top_50_teams=top_50_teams, challenges=CHALLENGES)


if __name__ == "__main__":
    app.debug = True
    app.run()
