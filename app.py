from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    games_new = [
        {"title": "Elder Ring: Nightreign", "image": "images/cover1.jpg"},
        {"title": "Elder Scrolls IV: Oblivion (remastered)",
            "image": "images/cover2.png"},
        {"title": "Schedule I", "image": "images/cover3.jpg"},
    ]

    games_recommended = [
        {"title": "Hollow Knight", "image": "images/cover4normal.png"},
        {"title": "Deltarune", "image": "images/cover5.png"},
        {"title": "Outer Wilds", "image": "images/cover6.png"},
    ]

    genres = [
        {"title": "RPG", "image": "images/rpg-game.png"},
        {"title": "ACTION", "image": "images/action-movie.png"},
        {"title": "HORROR", "image": "images/horror.png"},
        {"title": "RACING", "image": "images/racing.png"},
        {"title": "FPS", "image": "images/fps.png"},
        {"title": "strategy", "image": "images/strategy.png"},

    ]

    return render_template("index.html", new_games=games_new, recommended_games=games_recommended, genre_type=genres)


if __name__ == '__main__':
    app.run(debug=True)
