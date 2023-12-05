from flask import Flask, render_template, jsonify
#from flask import request
import pandas as pd
from surprise import Dataset
from surprise import Reader
from load_data import data
from recommender import algo
from surprise import SVD
from db import *

app = Flask(__name__)
THRESHOLD = 0.4
plays = getPlays()

@app.route("/")
def main():
    plays = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT playID, playTitle, playCompany, published FROM plays")
    for row in cursor.fetchall():
        plays.append({"id": row[0], "title": row[1], "company": row[2], "published": row[3]})
    conn.close()
    return render_template("plays.html", plays = plays)

@app.route("/knn/<user>/<int:item>")
def knn(user, item):
    prediction = algo.predict(user, item)
    return jsonify(prediction)

@app.route("/knn/<user>")
def knn2(user):
    recommendations = [algo.predict(user, pID) for pID in plays if algo.predict(user, pID).est>THRESHOLD]
    # for pID in plays:
    #     prediction = algo.predict(user, pID)
    #     recommendations.append(prediction.est)
    return jsonify(recommendations)

@app.route("/svd")
def svdSingle():
    svd = SVD(verbose=True, n_epochs=30)
    modelTrain(svd)
    predictions = svd.predict(uid='8', iid=2284)
    return jsonify(predictions)

@app.route("/svd/<user>")
def svd(user):
    svd = SVD(verbose=True, n_epochs=30)
    modelTrain(svd)
    recommendations = [svd.predict(user, pID) for pID in plays if svd.predict(user, pID).est>THRESHOLD]
    return jsonify(recommendations)

@app.route("/history/<int:user_id>")
def history(user_id):
    return jsonify(getUserHistory(user_id))

@app.route("/history")
def history_dict():
    return jsonify(getUserHistoryList())

@app.route("/train")
def train():
    modelTrain(algo)
    return jsonify('ok')

def modelTrain(model):
    ratings_dict = getUserHistoryList()
    df = pd.DataFrame(ratings_dict)
    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(df[["user_id", "object_id", "historyRating"]], reader)
    trainingSet = data.build_full_trainset()
    model.fit(trainingSet)
    return 'ok';

if(__name__ == "__main__"):
    app.run(debug=True)