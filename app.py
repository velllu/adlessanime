from flask import Flask, render_template
from flask import request
import bs4, requests, webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search')
def search():
    url = requests.get("https://www.animeworld.tv/search?keyword=" + request.args.get("search"))
    soup = bs4.BeautifulSoup(url.text, "html.parser")

    imagesHTML = soup.find_all("img", loading="lazy") # All the <img> elements of the anime covers
    images = [] # All urls to the images collected in a list
    for image in imagesHTML:
        images.append(image.get("src"))
        
    animeNames = [] # Names of anime (e.g. "Naruto Shippuden")
    animeLinks = [] # URLs that redirect to the anime
    for anime in soup.find_all("a", class_="name"): # Every <a> that contains useful data
        animeNames.append(anime.get("data-jtitle"))
        animeLinks.append(anime.get("href").replace("play/", "episodes?anime="))

    return render_template("search.html", anime_names=animeNames, anime_links=animeLinks, anime_images=images, len=len)

@app.route('/episodes')
def episodes():
    url = requests.get("https://www.animeworld.tv/play/" + request.args.get("anime"))
    soup = bs4.BeautifulSoup(url.text, "html.parser")

    animeNames = [] # e.g. 36-37, 340
    animeCodes = [] # e.g. /play?code=naruto-shippuden.3Q_-m/1Avo3

    for link in soup.find_all("a"):
        if link.get("data-episode-id") and link.get("data-id"):
            animeNames.append(link.decode_contents())
            animeCodes.append(link.get("href").replace("play/", "play?code="))

    indexToRemove = 0
    firstIndex = 0
    index = 0
    for animeName in animeNames:
        if index == 0:
            firstIndex = animeName
        
        if animeName == firstIndex:
            indexToRemove = index

        index = index + 1

    # Split the array after first repetition because for some reason episode_names/codes are repeated
    animeNames = animeNames[:len(animeNames)]
    animeCodes = animeCodes[:len(animeCodes)]
    
    return render_template("episodes.html", episode_names=animeNames, episode_codes=animeCodes, len=len)

@app.route("/play")
def play():
    url = requests.get("https://www.animeworld.tv/play/" + request.args.get("code"))
    soup = bs4.BeautifulSoup(url.text, "html.parser")

    animeVideoLink = soup.find("a", id="downloadLink").get("href")

    return render_template("play.html", video_link=animeVideoLink.replace("download-file.php?id=", ""), code=request.args.get("code"))

if __name__ == "__main__":
    app.run(debug=True, port=10138, host='0.0.0.0')
