from Modules.dataEngineering import dataEngineering
from Modules.modelKNN import modelKNN
from sys import exc_info
import pandas as pd

# from dataEngineering import dataEngineering
# from modelKmean import modelKmean


class userRequests(modelKNN, dataEngineering):
    def __init__(self):
        self.dataEngineering = dataEngineering()
        self.modelKNN = modelKNN()
    # def getMyWatchedMovies(self):
    #     self.getDatabase_dataFrame_byID()
    #     return myMovie 
        
    def recommendTop10Movie(self, email ,top_n=10):
        # Find User_Index in df_ratings 
        try:
            df_ratings = self.dataEngineering.loadRatings()['data']
            df_f_index = df_ratings.pivot(index='UserID', columns='MovieID' , values='userRating')

            userID = self.getUserbyEmail(email).UserID[0]
            print(userID, email)
            matrix = df_f_index[df_f_index.index == userID]

            prep_movies = self.modelKNN.predict_only_movies_unwatched(matrix).sort_values(by=['prep_Rating'], ascending=False).iloc[:top_n]
            prep_movies.drop(columns=['UserID'], inplace=True, axis=1)
            prep_movies = prep_movies.values.tolist()
            
        except IndexError:
            txt = (f'UserID: {userID} not in database')
            return {'status':False, 'data':txt}
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print('Recommend Movies-> Recommend: ', err)
            return {'status': False, 'data': err}
        else:
            return {'status':True, 'data':prep_movies}
        
    def getUserbyEmail(self, email):
        userID = self.dataEngineering.getUserbyEmail(email)['data']
        return userID
