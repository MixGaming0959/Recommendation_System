import joblib
from sys import exc_info 

class saveLoadModels:
    def save(self, filename, data):
        try:
            print('saveLoadFiles -> save: Trying to save \"' + filename + '.pkl\" file...')
            file = open('models/' + filename + '.pkl', 'wb')
            joblib.dump(data, file)
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print('saveLoadFiles -> save: ', err)
            file.close()
            return {'status': False, 'data': err}
        else:
            file.close()
            print('saveLoadFiles -> save: File \"' + filename + '.pkl\" saved successfully.')
            return {'status': True}
        
    def load(self, filename):
        try:
            # print('saveLoadFiles -> load: Trying to load \"' + filename + '.pkl\" file...')
            file = open('models/' + filename + '.pkl', 'rb')
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print(err)
            file.close()
            return {'status': False, 'data': err}
        else:
            data = joblib.load(file)
            file.close()
            # print('saveLoadFiles -> load: File \"' + filename + '.pkl\" loaded successfully.')
            return {'status': True, 'data': data}