import pandas as pd
from sys import exc_info
import sqlite3

import warnings
warnings.filterwarnings('ignore')

class InvalidInputError(Exception):
    pass

class dataEngineering:
    def __init__(self):
        self.ratings = None
        self.movies = None
        self.users = None

        self.n_components = 1
    
    def load_Filter_Ratings(self, from_loc = r'D:\Coding\Machine_Learning\Recommendation_System\input', table_name='filtered_ratings', limit=None):
        
        status, data = self.loadDatabase_dataFrame(from_loc, table_name, limit)

        return {'status': status, 'data': data}

    def loadRatings(self, from_loc = r'D:\Coding\Machine_Learning\Recommendation_System\input', table_name='ratings', limit=None):
        status, data = True, self.ratings
        if data is None:
            status, data = self.loadDatabase_dataFrame(from_loc, table_name, limit)
        return {'status': status, 'data': data}

    def loadUsers(self, from_loc = r'D:\Coding\Machine_Learning\Recommendation_System\input', table_name='users', limit=None):
        status, data = True, self.users
        if data is None:
            status, data = self.loadDatabase_dataFrame(from_loc, table_name, limit)
        return {'status': status, 'data': data}
    
    def loadMovies(self, from_loc = r'D:\Coding\Machine_Learning\Recommendation_System\input', table_name='movies', limit=None):
        status, data = True, self.movies
        if data is None:
            status, data = self.loadDatabase_dataFrame(from_loc, table_name, limit)
        return {'status': status, 'data': data}
        
    def getUser(self, uid, from_loc = r'D:\Coding\Machine_Learning\Recommendation_System\input', table_name='movies', limit=None):
        status, data = self.getDatabase_dataFrame_byID(id=uid, columns='UserID', from_loc=from_loc, table_name=table_name, limit=limit)

        return {'status': status, 'data': data}
  
    def loadDatabase_dataFrame(self, from_loc, table_name, limit=None):
        from_loc += "/" + table_name + ".db"
        
        try:
            if (limit is not None and limit < 0):
                raise InvalidInputError("Limit must be greater than 0")

            conn = sqlite3.connect(from_loc)
            query = None
            query = f'SELECT * FROM {table_name}'
            if limit is not None:
                query += f' LIMIT {limit}'
            df = pd.read_sql(query, conn)
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print('LoadDatabase -> Load: ', err)
            return [False, err]
        else:
            conn.close()
            return [True, df]
    
    def getDatabase_dataFrame_byID(self, id, columns, from_loc, table_name, limit=None):
        from_loc += "/" + table_name + ".db"

        try:
            if (limit is None):
                pass
            elif ( not isinstance(limit, int) ):
                raise InvalidInputError("Limit must be integers")
            elif ( limit is not None and limit <= 0 ):
                raise InvalidInputError("Limit must be greater than or equal to 0")

            conn = sqlite3.connect(from_loc)
            query = f'SELECT * FROM {table_name} WHERE {columns} = \'{id}\''
            if limit is not None:
                query += f' LIMIT {limit}'
            df = pd.read_sql(query, conn)
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print('LoadDatabase -> Load: ', err)
            return [False, err]
        else:
            conn.close()
            return [True, df]
        
        