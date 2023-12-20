from flask import Flask, render_template, request

import animeworld

app = Flask(__name__)


# TODO: Handle queries when they are blank

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    source = animeworld.AnimeWorld()

    title = str(request.args.get("search"))
    animes = source.get_search(title)

    return render_template("search.html", animes=animes)

@app.route("/episodes")
def episodes():
    source = animeworld.AnimeWorld()

    anime_id = str(request.args.get("anime"))
    episode_data = source.get_episodes(anime_id)

    return render_template(
        "episodes.html",
        episode_data=episode_data,
        anime_id=anime_id,
        enumerate=enumerate,
    )

@app.route("/play")
def play():
    source = animeworld.AnimeWorld()

    episode = str(request.args.get("episode"))
    anime = str(request.args.get("anime"))

    return render_template(
        "play.html",
        download_link=source.get_video_url(anime, episode),
        anime_id=anime,
        episode_id=episode,
    )

if __name__ == "__main__":
    app.run(debug=True, port=10138, host='0.0.0.0')
