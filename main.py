from flask import Flask, jsonify, request

from storage import all_articles, liked_articles, not_liked_articles, did_not_watch
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask(__name__)

@app.route("/get-article")
def get_article():
    return jsonify({
        "data":all_articles[0],
        "status":"success"
    }),

@app.route("/liked-articles", methods=["POST"])
def liked_article():
    article = all_articles[0]
    liked_articles.append(article)
    return jsonify({
        "status":"success"
    }),

@app.route("/unliked-articles", methods=["POST"])
def unliked_article():
    article = all_articles[0]
    not_liked_articles.append(article)
    return jsonify({
        "status":"success"
    }),

@app.route("/did-not-watch", methods=["POST"])
def did_not_watch():
    article = all_articles[0]
    did_not_watch.append(article)
    return jsonify({
        "status":"success"
    }),

@app.route("/recommended-movie")
def recommended_movie():
    all_recommended = []
    for liked_movie in liked_articles:
        output=get_recommendations(liked_movie[19])
        for data in output:
            all_recommended.append(data)

    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended, _ in itertools.groupby(all_recommended))

    movie_data = []

    for recommended in all_recommended:
        _d = {
            "title":recommended[0],
            "release_date":recommended[1],
            "duration":recommended[2],
            "rating":recommended[3],
            "overview":recommended[4]
        }
        movie_data.append(_d)

    return jsonify({
         "data": movie_data,
         "status": "success"
    })

if __name__ == "__main__":
    app.run()