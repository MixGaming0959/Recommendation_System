from Modules.dataEngineering import dataEngineering
from Modules.modelKNN import modelKNN
import pandas as pd

# from dataEngineering import dataEngineering
# from modelKmean import modelKmean


class userRequests(dataEngineering, modelKNN):
    def __init__(self):
        pass
    
    def getMyWatchedMovies(self):
        from_loc = r'D:\Coding\Machine_Learning\Recommendation_System\test\input'
        self.getDatabase_dataFrame_byID(userID, 'movies', )
        return myMovie 
    
    def predict_only_movies_unwatched(self, userId):
        if userId not in self.ratings['UserID'].values:
            return {'status':False, 'data': None}
        
        df_ratings = self.ratings.copy()
        df_ratings = df_ratings[df_ratings.UserID == userId]

        matrix = modelKNN().run_model(df_ratings = df_ratings)
        return {'status':True, 'data': matrix}
        
    def recommendTop10MoviesbyUserId(self, userId):
        movies = self.movies.copy()
        temp = self.run_model_Kmean(userId)
        status, matrix = temp['status'], temp['data']
        if not status:
            return {'status':False,'data':'You haven\'t voted for any movie yet.'}
    
        myClustererId = int(matrix.cluster[matrix.index == userId])

        recommendMovies = self.groupCluster[str(myClustererId)]
        output_text = "\nYour Cluster ID: %d\n"%myClustererId
        output_text += "### Top 10 Movies Recommend for You\n\n"
        output_text += "| Title | Rating |\n"
        output_text += "|-------|--------|\n"
        for i in range(0, len(recommendMovies)):
            id = recommendMovies[i][0]
            title = (movies[movies['MovieID'] == id].Title.values)[0]
            output_text += "| " + title + "\t | " + "{:.2f}".format((recommendMovies[i][1])) + " |\n"
        return {'status': True, 'data' : output_text}
