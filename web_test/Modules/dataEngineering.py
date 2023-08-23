import pandas as pd
from sys import exc_info
import sqlite3

import warnings
warnings.filterwarnings('ignore')

class InvalidInputError(Exception):
    pass

class dataEngineering:
    
    def load_Filter_Ratings(self, from_loc = r'D:\Coding\Machine_Learning\Recommendation_System\test\input', table_name='filtered_ratings', limit=None):
        tmp = self.loadDatabase_dataFrame(from_loc, table_name, limit)
        status, data = tmp['status'], tmp['data']

        status, data = tmp['status'], tmp['data']

        return {'status': status, 'data': data}

    def loadRatings(self, from_loc = r'D:\Coding\Machine_Learning\Recommendation_System\test\input', table_name='ratings', limit=None):
        tmp = self.loadDatabase_dataFrame(from_loc, table_name, limit)
        status, data = tmp['status'], tmp['data']

        return {'status': status, 'data': data}

    def loadUsers(self, from_loc = r'D:\Coding\Machine_Learning\Recommendation_System\test\input', table_name='users', limit=None):
        tmp = self.loadDatabase_dataFrame(from_loc, table_name, limit)

        status, data = tmp['status'], tmp['data']

        return {'status': status, 'data': data}
    
    def loadMovies(self, from_loc = r'D:\Coding\Machine_Learning\Recommendation_System\test\input', table_name='movies', limit=None):
        tmp = self.loadDatabase_dataFrame(from_loc, table_name, limit)

        status, data = tmp['status'], tmp['data']

        return {'status': status, 'data': data}
        
    def getUserbyEmail(self, email, from_loc = r'D:\Coding\Machine_Learning\Recommendation_System\test\input', table_name='users', limit=None):
        tmp = self.getDatabase_dataFrame_byID(id=email, columns='Email', from_loc=from_loc, table_name=table_name, limit=limit)

        status, data = tmp['status'], tmp['data']

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
            return {'status': False, 'data': err}
        else:
            conn.close()
            return {'status': True, 'data': df}
    
    def getDatabase_dataFrame_byID(self, id, columns, from_loc, table_name, limit=None):
        from_loc += "/" + table_name + ".db"

        try:
            if id == None or (limit is not None and not isinstance(limit, int)):
                raise InvalidInputError("ID and limit must be integers")
            if limit is not None and limit <= 0:
                raise InvalidInputError("ID and limit must be greater than or equal to 0")

            conn = sqlite3.connect(from_loc)
            query = f'SELECT * FROM {table_name} WHERE {columns} = \'{id}\''
            if limit is not None:
                query += f' LIMIT {limit}'
            df = pd.read_sql(query, conn)
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print('LoadDatabase -> Load: ', err)
            return {'status': False, 'data': err}
        else:
            conn.close()
            return {'status': True, 'data': df}
        