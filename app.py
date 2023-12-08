from flask import Flask, render_template, jsonify
#from flask import request
import pandas as pd
from surprise import Dataset
from surprise import Reader
from load_data import data
from recommender import algo
from surprise import SVD
from pearson import getRecommendations
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

@app.route("/recommendations/<user>")
def recommendations(user):
    #PREFS = getUserHistoryDict()  #for real data from DB
    PREFS = {2: {5: 1, 6: 1, 7: 0, 8: 1, 9: 0, 10: 1, 120: 1, 490: 0, 576: 0, 605: 0, 610: 0, 618: 0, 671: 1, 718: 0, 735: 1, 906: 0, 2284: 1, 684: 1}, 8: {5: 1, 6: 0, 7: 0, 8: 1, 9: 0, 10: 1, 120: 0, 490: 0, 576: 0, 605: 0, 610: 0, 618: 0, 671: 1, 718: 0, 735: 1, 906: 0, 2153: 0, 2306: 0}, 10: {47: 0, 48: 0, 67: 0, 219: 0, 2243: 0, 2306: 0, 2337: 0}, 15: {482: 1, 538: 0, 824: 1}}
    recommendations = getRecommendations(PREFS, int(user))
    # CREATE LIST WITH PLAY IDs THAT SIMILAR USERS RECOMMEND  
    playIDs = [v for k,v in recommendations if k==1]  
    return jsonify(playIDs)

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