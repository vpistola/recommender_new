import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import cross_validate
from load_data import data

svd = SVD(verbose=True, n_epochs=30)
# cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)
trainset = data.build_full_trainset()
svd.fit(trainset)

predictions = svd.predict(uid='E', iid=2)
print(predictions)