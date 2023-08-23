import warnings
warnings.filterwarnings('ignore')
from sys import exc_info
import pandas as pd
from Modules.saveLoadModels import saveLoadModels

from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import KNNWithMeans
from surprise import accuracy


class modelKNN(KNNWithMeans, saveLoadModels):
    def __init__(self):
        self.reader = Reader(rating_scale=(1, 5))
        self.options = {
                        'bsl_options': {'learning_rate': 0.0005, 'method': 'sgd'},
                        'sim_options': {'name': 'cosine', 'user_based': True}
                       }
    
    # train to save model
    def train_KNNmodel(self, df, k_group=5):
        try:
            data = Dataset.load_from_df(df.stack().reset_index(), self.reader)
            X_train, X_test = train_test_split(data, test_size=0.2, random_state=42)

            model = KNNWithMeans(
                sim_options=self.options['sim_options'], 
                bsl_options=self.options['bsl_options']
            )
            model.fit(X_train)

            predictions = model.predict(X_test)
            rmse = accuracy.rmse(predictions)
            mae = accuracy.mae(predictions)

            data = {'rmse':rmse, 'mae':mae}

            self.save('knn_model', model)
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print('Train Model -> Train: ', err)
            return {'status': False, 'data': err}
        else:
            return {'status': True, 'data': data}
    
    def predict_model_n_index(self, matrix):
        try:
            matrix = matrix.copy()
            u_col = 0
            model = self.importModel()
            for u_id, row in matrix.iterrows():
                for m_col, item in enumerate(row):
                    m_id = matrix.columns[m_col]
                    if pd.isnull(item):
                        prep_rating = round(model.predict(u_id, m_id).est, 4)
                        matrix.iloc[u_col][m_id] = prep_rating
                u_col += 1
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print('Run Model -> Run: ', err)
            return {'status': False, 'data': err}
        else:
            return matrix
    
    def predict_only_movies_unwatched(self, matrix):
        try:
            matrix = matrix.copy()
            model = self.importModel()
            ratings = []
            u_col = 0
            
            for u_id, row in matrix.iterrows():
                for m_col, item in enumerate(row):
                    m_id = matrix.columns[m_col]
                    if pd.isnull(item):
                        prep_rating = round(model.predict(u_id, m_id).est, 4)
                        ratings.append([u_id, m_id, prep_rating])
                        matrix.iloc[u_col][m_id] = prep_rating
                u_col += 1
            
            recomment_unwatched = pd.DataFrame(ratings, columns=['UserID', 'MovieID', 'prep_Rating'])
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print('Predict Movies -> Predict: ', err)
            return {'status': False, 'data': err}
        else:
            return recomment_unwatched
    
    def importModel(self):
        return self.load('knn_model')['data']
