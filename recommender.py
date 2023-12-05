from surprise import KNNWithMeans
from load_data import data

# To use item-based cosine similarity
sim_options = {
    "name": "cosine",
    "user_based": True,  # Compute  similarities between items
}
algo = KNNWithMeans(sim_options=sim_options)

# trainingSet = data.build_full_trainset()
# algo.fit(trainingSet)
# prediction = algo.predict('E', 2)
# print(prediction.r_ui)